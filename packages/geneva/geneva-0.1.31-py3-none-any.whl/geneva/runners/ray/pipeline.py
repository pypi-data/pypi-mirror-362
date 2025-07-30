# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright The Geneva Authors

import contextlib
import functools
import hashlib
import json
import logging
import random
import uuid
from collections.abc import Iterator
from typing import Any, cast

import attrs
import bidict
import cloudpickle
import lance
import pyarrow as pa
import ray.actor
import ray.exceptions
import ray.util.queue
from ray import ObjectRef
from tqdm.std import tqdm as TqdmType  # noqa: N812

from geneva.apply import (
    CheckpointingApplier,
    plan_copy,
    plan_read,
)
from geneva.apply.applier import BatchApplier
from geneva.apply.multiprocess import MultiProcessBatchApplier
from geneva.apply.simple import SimpleApplier
from geneva.apply.task import BackfillUDFTask, CopyTableTask, MapTask, ReadTask
from geneva.checkpoint import CheckpointStore
from geneva.debug.logger import CheckpointStoreErrorLogger
from geneva.job.config import JobConfig
from geneva.packager import UDFPackager
from geneva.query import (
    MATVIEW_META_BASE_DBURI,
    MATVIEW_META_BASE_TABLE,
    MATVIEW_META_BASE_VERSION,
    MATVIEW_META_QUERY,
    GenevaQuery,
    GenevaQueryBuilder,
)
from geneva.runners.ray.actor_pool import ActorPool
from geneva.runners.ray.kuberay import _ray_job_status
from geneva.runners.ray.raycluster import CPU_ONLY_NODE, ProgressTracker, ray_tqdm
from geneva.runners.ray.writer import FragmentWriter
from geneva.table import JobFuture, Table, TableReference
from geneva.tqdm import tqdm
from geneva.transformer import UDF

_LOG = logging.getLogger(__name__)

_SIMULATE_WRITE_FAILURE = False


@contextlib.contextmanager
def _simulate_write_failure(flag: bool) -> Iterator[None]:
    global _SIMULATE_WRITE_FAILURE
    current = _SIMULATE_WRITE_FAILURE
    try:
        _SIMULATE_WRITE_FAILURE = flag
        yield
    finally:
        _SIMULATE_WRITE_FAILURE = current


@ray.remote
@attrs.define
class ApplierActor:
    applier: CheckpointingApplier

    def __ray_ready__(self) -> None:
        pass

    def run(self, task) -> tuple[ReadTask, str]:
        return task, self.applier.run(task)


ApplierActor: ray.actor.ActorClass = cast("ray.actor.ActorClass", ApplierActor)


def _get_fragment_dedupe_key(uri: str, frag_id: int, map_task: MapTask) -> str:
    key = f"{uri}:{frag_id}:{map_task.checkpoint_key()}"
    return hashlib.sha256(key.encode()).hexdigest()


def _run_column_adding_pipeline(
    map_task: MapTask,
    checkpoint_store: CheckpointStore,
    config: JobConfig,
    dst: TableReference,
    input_plan: Iterator[ReadTask],
    job_id: str | None,
    applier_concurrency: int = 8,
    *,
    intra_applier_concurrency: int = 1,
    batch_applier: BatchApplier | None = None,
    use_cpu_only_pool: bool = False,
    fragment_tracker=None,
    writer_tracker=None,
    worker_tracker=None,
    where=None,
) -> None:
    """
    Run the column adding pipeline.

    Args:
    * use_cpu_only_pool: If True will force schedule cpu-only actors on cpu-only nodes.

    """
    cnt_batches = len(input_plan)
    ds = dst.open().to_lance()
    fragments = ds.get_fragments()
    cnt_fragments = len(fragments)
    _LOG.info(
        f"Pipeline executing on {cnt_batches} batches over "
        f"{cnt_fragments} table fragments"
    )

    plan_tracker = fragment_tracker or ProgressTracker.remote()
    plan_tracker.set_total.remote(cnt_batches)
    plan = ray_tqdm(input_plan, plan_tracker)

    # TODO read prefix f"[{dst.table_name} - {map_task.name()}]"
    writer_tracker = writer_tracker or ProgressTracker.remote(len(fragments))
    writer_tracker.set_total.remote(len(fragments))
    ray_tqdm(fragments, writer_tracker)
    # TODO descriptions f"{pbar_prefix} Writing Fragments"

    job_id = job_id or uuid.uuid4().hex

    if batch_applier is None:
        if intra_applier_concurrency > 1:
            batch_applier = MultiProcessBatchApplier(
                num_processes=intra_applier_concurrency
            )
        else:
            batch_applier = SimpleApplier()

    applier = CheckpointingApplier(
        map_task=map_task,
        batch_applier=batch_applier,
        checkpoint_store=checkpoint_store,
        error_logger=CheckpointStoreErrorLogger(job_id, checkpoint_store),
    )

    actor = ApplierActor

    # actor.options can only be called once, we must pass all override args
    # in one shot
    args = {
        "num_cpus": map_task.num_cpus() * intra_applier_concurrency,
    }
    if map_task.is_cuda():
        args["num_gpus"] = 1
    elif use_cpu_only_pool:
        _LOG.info("Using CPU only pool for applier, setting %s to 1", CPU_ONLY_NODE)
        args["resources"] = {CPU_ONLY_NODE: 1}

    if map_task.memory():
        args["memory"] = map_task.memory() * intra_applier_concurrency
    actor = actor.options(**args)

    worker_tracker = worker_tracker or ProgressTracker.remote()
    worker_tracker.set_total.remote(applier_concurrency)
    pool = ActorPool(
        functools.partial(actor.remote, applier=applier),
        applier_concurrency,
        worker_tracker=worker_tracker,
    )

    # kick off the applier actors
    # TODO description f"{pbar_prefix} Applying UDFs"
    applier_iter = pool.map_unordered(
        lambda actor, value: actor.run.remote(value), plan
    )

    # setup the fragment writers (many ReadTasks can feed a single fragement writer)
    writers = {}
    writer_queues: dict[int, ray.util.queue.Queue] = {}
    writer_futs_to_id = bidict.bidict()
    writer_task_cache = {}

    output_columns = [
        field.name for field in map_task.output_schema() if field.name != "_rowaddr"
    ]

    def _make_writer(frag_id) -> None:
        queue = ray.util.queue.Queue()
        writer = FragmentWriter.remote(
            ds.uri,
            output_columns,
            checkpoint_store,
            frag_id,
            queue,
            align_physical_rows=True,
            where=where,
        )
        writer_queues[frag_id] = queue
        writers[frag_id] = writer
        writer_futs_to_id[writer.write.remote()] = frag_id

    def _shutdown_writer(frag_id) -> None:
        actor_handle: ray.actor.ActorHandle = writers[frag_id]
        ray.kill(actor_handle)
        del writers[frag_id]
        writer_queue: ray.util.queue.Queue = writer_queues[frag_id]
        writer_queue.shutdown()
        del writer_queues[frag_id]
        fut = writer_futs_to_id.inverse[frag_id]
        del writer_futs_to_id[fut]

    def _restart_writer(frag_id) -> None:
        while True:
            try:
                _shutdown_writer(frag_id)
                _make_writer(frag_id)
                for task in writer_task_cache[frag_id]:
                    writer_queues[frag_id].put(task)
                _LOG.info("Restarted writer for fragment %d", frag_id)
                break
            # we need to keep retrying if our queue gets killed while we are
            # trying to put. There isn't a "safe_put_queue" method because we
            # could stack overflow from
            # _restart_writer -> safe_put_queue -> _restart_writer -> ...
            except (
                ray.exceptions.ActorDiedError,
                ray.exceptions.ActorUnavailableError,
            ):
                _LOG.exception("Failed to commit fragments, restarting writer")
                continue

    pending_fragments: list[tuple[int, lance.fragment.DataFile]] = []

    dst_read_version = ds.version

    def _do_commit(commit_granularity: int) -> None:
        nonlocal pending_fragments, dst_read_version

        if len(pending_fragments) >= commit_granularity:
            operation = lance.LanceOperation.DataReplacement(
                replacements=[
                    lance.LanceOperation.DataReplacementGroup(
                        fragment_id=frag_id,
                        new_file=new_file,
                    )
                    for frag_id, new_file in pending_fragments
                ]
            )

            lance.LanceDataset.commit(ds.uri, operation, read_version=dst_read_version)
            dst_read_version += 1
            pending_fragments = []

    def _commit(frag_id: int, fut: ObjectRef, commit_granularity: int) -> None:
        """Commit the fragment writer and checkpoint the result.

        This is called when the writer future is ready.
        """
        nonlocal pending_fragments
        _LOG.debug("Committing fragment id: %d", frag_id)

        try:
            # ray.get can hang here if not all fragments have ReadTasks
            fut_frag_id, new_file = ray.get(fut)  # this potentially livelocks
            assert fut_frag_id == frag_id
            pending_fragments.append((frag_id, new_file))
        except (ray.exceptions.ActorDiedError, ray.exceptions.ActorUnavailableError):
            _restart_writer(frag_id)
            return

        _do_commit(commit_granularity)
        _shutdown_writer(frag_id)
        del writer_task_cache[frag_id]

        dedupe_key = _get_fragment_dedupe_key(ds.uri, frag_id, map_task)
        # store file name in case of a failure or delete and recalc reuse.
        checkpoint_store[dedupe_key] = pa.RecordBatch.from_pydict(
            {"file": new_file.path}
        )
        writer_tracker.increment.remote(1)

    for item in applier_iter:
        task: ReadTask = item[0]
        result = item[1]

        frag_id = task.dest_frag_id()
        if frag_id not in writers:
            _LOG.debug("Creating writer for fragment %d", frag_id)
            _make_writer(frag_id)
            writer_task_cache[frag_id] = []

        writer_task_cache[frag_id].append((task.dest_offset(), result))
        try:
            writer_queues[frag_id].put((task.dest_offset(), result))
        except (ray.exceptions.ActorDiedError, ray.exceptions.ActorUnavailableError):
            _restart_writer(frag_id)
        # save the task result before the fragment is committed
        # in the event the fragment writer fails we can restart it easily

        # FAULT INJECTION: simulate write failure for testing
        if _SIMULATE_WRITE_FAILURE and random.random() < 0.5:
            if random.random() < 0.5:
                ray.kill(writers[frag_id])
            else:
                ray.kill(writer_queues[frag_id].actor)

        ready, _ = ray.wait(list(writer_futs_to_id.keys()), timeout=0)
        for fut in ready:
            frag_id = writer_futs_to_id[fut]
            _commit(frag_id, fut, config.commit_granularity)

    pool.shutdown()

    # Force commit the remaining fragments in the buffer.
    _do_commit(1)

    # commit any remaining fragments
    # need to keep retry until all fragments are committed
    while writer_futs_to_id:
        for fut, frag_id in list(writer_futs_to_id.items()):
            # check for ready writers, before attempting to commit.  Without this
            # the get _commit will deadlock the writers, even with unit tes timeouts.

            # TODO: make this wait wait on all futures and act on the ready ones.
            ready, _ = ray.wait(
                [fut], timeout=5.0
            )  # careful: if writer is stuck, this loops forever
            if not ready:
                _LOG.debug(f"Waiting on {len(writer_futs_to_id)} writers")
                continue
            # More aggressively commit restarted fragments
            _commit(frag_id, fut, 1)


def run_ray_copy_table(
    dst: TableReference,
    packager: UDFPackager,
    checkpoint_store: CheckpointStore | None = None,
    *,
    job_id: str | None = None,
    concurrency: int = 8,
    batch_size: int | None = None,
    task_shuffle_diversity: int | None = None,
    commit_granularity: int | None = None,
    **kwargs,
) -> None:
    # prepare job parameters
    config = JobConfig.get().with_overrides(
        batch_size=batch_size,
        task_shuffle_diversity=task_shuffle_diversity,
        commit_granularity=commit_granularity,
    )

    checkpoint_store = checkpoint_store or config.make_checkpoint_store()

    dst_schema = dst.open().schema
    if dst_schema.metadata is None:
        raise Exception("Destination dataset must have view metadata.")
    src_dburi = dst_schema.metadata[MATVIEW_META_BASE_DBURI.encode("utf-8")].decode(
        "utf-8"
    )
    src_name = dst_schema.metadata[MATVIEW_META_BASE_TABLE.encode("utf-8")].decode(
        "utf-8"
    )
    src_version = int(
        dst_schema.metadata[MATVIEW_META_BASE_VERSION.encode("utf-8")].decode("utf-8")
    )
    src = TableReference(db_uri=src_dburi, table_name=src_name, version=src_version)
    query_json = dst_schema.metadata[MATVIEW_META_QUERY.encode("utf-8")]
    query = GenevaQuery.model_validate_json(query_json)

    src_table = src.open()
    schema = GenevaQueryBuilder.from_query_object(src_table, query).schema

    job_id = job_id or uuid.uuid4().hex

    column_udfs = query.extract_column_udfs(packager)

    # take all cols (excluding some internal columns) since contents are needed to feed
    # udfs or copy src table data
    input_cols = [
        n for n in src_table.schema.names if n not in ["__is_set", "__source_row_id"]
    ]

    plan = plan_copy(
        src,
        dst,
        input_cols,
        batch_size=config.batch_size,
        task_shuffle_diversity=config.task_shuffle_diversity,
    )

    map_task = CopyTableTask(
        column_udfs=column_udfs, view_name=dst.table_name, schema=schema
    )

    _run_column_adding_pipeline(
        map_task,
        checkpoint_store,
        config,
        dst,
        plan,
        job_id,
        concurrency,
        **kwargs,
    )


def dispatch_run_ray_add_column(
    table_ref: TableReference,
    col_name: str,
    *,
    read_version: int | None = None,
    concurrency: int = 8,
    batch_size: int | None = None,
    task_shuffle_diversity: int | None = None,
    commit_granularity: int | None = None,
    where: str | None = None,
    **kwargs,
) -> JobFuture:
    """
    Dispatch the Ray add column operation to a remote function.
    This is a convenience function to allow calling the remote function directly.
    """

    db = table_ref.open_db()
    hist = db._history
    job = hist.launch(table_ref.table_name, col_name, where=where, **kwargs)

    fragment_tracker = ProgressTracker.remote()
    writer_tracker = ProgressTracker.remote()
    worker_tracker = ProgressTracker.remote()

    obj_ref = run_ray_add_column_remote.remote(
        table_ref,
        col_name,
        read_version=read_version,
        job_id=job.job_id,
        concurrency=concurrency,
        batch_size=batch_size,
        task_shuffle_diversity=task_shuffle_diversity,
        commit_granularity=commit_granularity,
        where=where,
        fragment_tracker=fragment_tracker,
        writer_tracker=writer_tracker,
        worker_tracker=worker_tracker,
        **kwargs,
    )
    # object ref is only available here
    hist.set_object_ref(job.job_id, cloudpickle.dumps(obj_ref))
    return RayJobFuture(
        job_id=job.job_id,
        ray_obj_ref=obj_ref,
        fragment_tracker=fragment_tracker,
        writer_tracker=writer_tracker,
        worker_tracker=worker_tracker,
    )


def validate_backfill_args(
    tbl: Table,
    col_name: str,
    udf: UDF | None = None,
    input_columns: list[str] | None = None,
) -> None:
    """
    Validate the arguments for the backfill operation.
    This is a placeholder function to ensure that the arguments are valid.
    """
    if col_name not in tbl._ltbl.schema.names:
        raise ValueError(
            f"Column {col_name} is not defined this table.  "
            "Use add_columns to register it first"
        )

    if udf is None:
        from geneva.runners.ray.__main__ import fetch_udf

        udf_spec = fetch_udf(tbl, col_name)
        udf = tbl._conn._packager.unmarshal(udf_spec)

    if input_columns is None:
        field = tbl._ltbl.schema.field(col_name)
        input_columns = json.loads(
            field.metadata.get(b"virtual_column.udf_inputs", "null")
        )
    else:
        udf._input_columns_validator(None, input_columns)


@ray.remote
def run_ray_add_column_remote(
    table_ref: TableReference,
    col_name: str,
    *,
    job_id: str | None = None,
    input_columns: list[str] | None = None,
    udf: UDF | None = None,
    where: str | None = None,
    fragment_tracker,
    writer_tracker,
    worker_tracker,
    **kwargs,
) -> None:
    """
    Remote function to run the Ray add column operation.
    This is a wrapper around `run_ray_add_column` to allow it to be called as a Ray
    task.
    """
    import geneva  # noqa: F401  Force so that we have the same env in next level down

    tbl = table_ref.open()
    hist = tbl._conn._history
    hist.set_running(job_id)
    try:
        validate_backfill_args(tbl, col_name, udf, input_columns)
        if udf is None:
            from geneva.runners.ray.__main__ import fetch_udf

            udf_spec = fetch_udf(tbl, col_name)
            udf = tbl._conn._packager.unmarshal(udf_spec)

        if input_columns is None:
            field = tbl._ltbl.schema.field(col_name)
            input_columns = json.loads(
                field.metadata.get(b"virtual_column.udf_inputs", "null")
            )

        from geneva.runners.ray.pipeline import run_ray_add_column

        checkpoint_store = tbl._conn._checkpoint_store
        run_ray_add_column(
            table_ref,
            input_columns,
            {col_name: udf},
            checkpoint_store=checkpoint_store,
            where=where,
            fragment_tracker=fragment_tracker,
            writer_tracker=writer_tracker,
            worker_tracker=worker_tracker,
            **kwargs,
        )
        hist.set_completed(job_id)
    except Exception as e:
        _LOG.exception("Error running Ray add column operation")
        hist.set_failed(job_id, str(e))
        raise e


def run_ray_add_column(
    table_ref: TableReference,
    columns: list[str] | None,
    transforms: dict[str, UDF],
    checkpoint_store: CheckpointStore | None = None,
    *,
    read_version: int | None = None,
    job_id: str | None = None,
    concurrency: int = 8,
    batch_size: int | None = None,
    task_shuffle_diversity: int | None = None,
    commit_granularity: int | None = None,
    where: str | None = None,
    writer_tracker=None,
    fragment_tracker=None,
    worker_tracker=None,
    **kwargs,
) -> None:
    # prepare job parameters
    config = JobConfig.get().with_overrides(
        batch_size=batch_size,
        task_shuffle_diversity=task_shuffle_diversity,
        commit_granularity=commit_granularity,
    )

    checkpoint_store = checkpoint_store or config.make_checkpoint_store()

    table = table_ref.open()
    uri = table.to_lance().uri

    # add pre-existing col if carrying previous values forward
    carry_forward_cols = list(set(transforms.keys()) & set(table.schema.names))
    _LOG.debug(f"carry_forward_cols {carry_forward_cols}")
    # this copy is necessary because the array extending updates inplace and this
    # columns array is directly referenced by the udf instance earlier
    cols = table.schema.names.copy() if columns is None else columns.copy()
    for cfcol in carry_forward_cols:
        # only append if cf col is not in col list already
        if cfcol not in cols:
            cols.append(cfcol)

    worker_tracker = worker_tracker or ProgressTracker.remote()
    rjs = _ray_job_status()
    worker_tracker.set.remote(rjs.get("ray_actors", 0))

    plan, pipeline_args = plan_read(
        uri,
        cols,
        batch_size=config.batch_size,
        read_version=read_version,
        task_shuffle_diversity=config.task_shuffle_diversity,
        where=where,
        **kwargs,
    )

    map_task = BackfillUDFTask(udfs=transforms, where=where)

    _LOG.info(
        f"starting backfill pipeline for {transforms} where='{where}'"
        f" with carry_forward_cols={carry_forward_cols}"
    )
    _run_column_adding_pipeline(
        map_task,
        checkpoint_store,
        config,
        table_ref,
        plan,
        job_id,
        concurrency,
        where=where,
        fragment_tracker=fragment_tracker,
        writer_tracker=writer_tracker,
        worker_tracker=worker_tracker,
        **pipeline_args,
    )


@attrs.define
class RayJobFuture(JobFuture):
    ray_obj_ref: ObjectRef = attrs.field()
    worker_tracker: ObjectRef | None = attrs.field(default=None)
    worker_pbar: TqdmType | None = attrs.field(default=None)
    fragment_tracker: ObjectRef | None = attrs.field(default=None)
    fragment_pbar: TqdmType | None = attrs.field(default=None)
    writer_tracker: ObjectRef | None = attrs.field(default=None)
    writer_pbar: TqdmType | None = attrs.field(default=None)

    def done(self, timeout: float = 0.0) -> bool:
        self.status()
        ready, _ = ray.wait([self.ray_obj_ref], timeout=timeout)
        done = bool(ready)
        if done:
            self.status()
        return done

    def result(self, timeout: float | None = None) -> Any:
        # TODO this can throw a ray.exceptions.GetTimeoutError if the task
        # does not complete in time, we should create a new exception type to
        # encapsulate Ray specifics
        self.status()
        return ray.get(self.ray_obj_ref, timeout=timeout)

    def status(self) -> None:
        if self.worker_tracker is not None:
            prog = ray.get(self.worker_tracker.get_progress.remote())
            n, total, done = prog["n"], prog["total"], prog["done"]
            if self.worker_pbar is None:
                _LOG.debug("starting worker tracker...")
                self.worker_pbar = tqdm(total=total, desc="Workers started")
            # sync the bar's count
            self.worker_pbar.total = total
            self.worker_pbar.n = n
            self.worker_pbar.refresh()
            if done:
                self.worker_pbar.close()

        if self.fragment_tracker is not None:
            prog = ray.get(self.fragment_tracker.get_progress.remote())
            n, total, done = prog["n"], prog["total"], prog["done"]
            if self.fragment_pbar is None:
                _LOG.debug("starting batchtracker...")
                self.fragment_pbar = tqdm(total=total, desc="Batches checkpointed")
            # sync the bar's count
            self.fragment_pbar.total = total
            self.fragment_pbar.n = n
            self.fragment_pbar.refresh()
            if done:
                self.fragment_pbar.close()

        if self.writer_tracker is not None:
            prog = ray.get(self.writer_tracker.get_progress.remote())
            n, total, done = prog["n"], prog["total"], prog["done"]
            if self.writer_pbar is None:
                _LOG.debug("starting fragment tracker...")
                self.writer_pbar = tqdm(total=total, desc="Fragments written")
            # sync the bar's count
            self.writer_pbar.total = total
            self.writer_pbar.n = n
            self.writer_pbar.refresh()
            if done:
                self.writer_pbar.close()
