# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright The Geneva Authors

import itertools
import logging
from collections.abc import Callable
from pathlib import Path
from typing import Any, NamedTuple

import lance
import pyarrow as pa
import pyarrow.compute as pc
import pytest
from lance.blob import BlobFile

try:
    # skip when tests depend on ray package and its not present
    from geneva.runners.ray.pipeline import RayJobFuture
except ImportError:
    import pytest

    pytest.skip("failed to import ray", allow_module_level=True)

import geneva
from geneva import connect, udf
from geneva.runners.ray.pipeline import RayJobFuture
from geneva.table import Table

_LOG = logging.getLogger(__name__)
_LOG.setLevel(logging.DEBUG)

SIZE = 17  # was 256
MAX_ROWS_PER_FILE = 5

try:
    import ray  #  noqa: F401
except ImportError:
    import pytest

    pytest.skip("failed to import geneva.runners.ray", allow_module_level=True)


@pytest.fixture(autouse=True)
def ray_cluster() -> None:
    ray.shutdown()
    ray.init(
        logging_config=ray.LoggingConfig(
            encoding="TEXT", log_level="DEBUG", additional_log_standard_attrs=["name"]
        ),
    )
    yield
    ray.shutdown()


@pytest.fixture
def tbl_path(tmp_path) -> Path:
    return tmp_path / "foo.lance"


def make_new_ds_a(tbl_path: Path) -> lance.dataset:
    # create initial dataset with only column 'a'
    data = {"a": pa.array(range(SIZE))}
    tbl = pa.Table.from_pydict(data)
    ds = lance.write_dataset(tbl, tbl_path, max_rows_per_file=MAX_ROWS_PER_FILE)
    return ds


class UDFTestConfig(NamedTuple):
    expected_recordbatch: dict[Any, Any]
    where: str | None = None


def int32_return_none(batch: pa.RecordBatch) -> pa.RecordBatch:
    return pa.RecordBatch.from_pydict(
        {"b": pa.array([None] * batch.num_rows, pa.int32())}
    )


def setup_table_and_udf_column(
    tmp_path: Path,
    shuffle_config,
    udf,
) -> Table:
    tbl_path = tmp_path / "foo.lance"
    make_new_ds_a(tbl_path)
    db = geneva.connect(str(tmp_path))
    tbl = db.open_table("foo")

    tbl.add_columns(
        {"b": udf},
        **shuffle_config,
    )
    _LOG.info(f"Table prebackfill at version {tbl.version}")
    return tbl


def backfill_and_verify(tbl, testcfg) -> None:
    fut = tbl.backfill_async("b", where=testcfg.where)
    while not fut.done(timeout=1):
        _LOG.info("Waiting for backfill to complete...")

    _LOG.info(f"Backfill job {fut.job_id} completed, checking results...")
    _LOG.info(f"{tbl._conn._history.jobs_table.to_arrow().to_pylist()}")

    tbl.checkout_latest()
    _LOG.info(f"completed backfill, now on version {tbl.version}")

    _LOG.info(
        f"actual={tbl.to_arrow().to_pydict()} expected={testcfg.expected_recordbatch}"
    )
    assert tbl.to_arrow().to_pydict() == testcfg.expected_recordbatch

    # Verify job history record seems reasonable
    hist = tbl._conn._history
    jr = hist.get(fut.job_id)[0]
    assert jr.status == "DONE"
    assert jr.object_ref is not None
    assert jr.table_name == tbl.name
    assert jr.column_name == "b"
    assert jr.launched_at is not None
    assert jr.completed_at is not None

    # Verify progress tracking in future seems right.
    assert fut.job_id is not None
    assert isinstance(fut, RayJobFuture)
    assert fut.ray_obj_ref is not None
    partitions = int((SIZE + MAX_ROWS_PER_FILE - 1) / MAX_ROWS_PER_FILE)
    assert fut.fragment_pbar.n == fut.fragment_pbar.total
    assert fut.fragment_pbar.n == partitions
    assert fut.writer_pbar.n == fut.writer_pbar.total
    assert fut.writer_pbar.n == partitions


# UDF argument validation tests


@udf(data_type=pa.int32())
def recordbatch_udf(batch: pa.RecordBatch) -> pa.Array:
    return batch["a"]


# Backfill tests with scalar return values


# 0.1 cpu so we don't wait for provisioning in the tests
@udf(data_type=pa.int32(), batch_size=8, num_cpus=1)
def times_ten(a) -> int:
    return a * 10


scalar_udftest = UDFTestConfig(
    {
        "a": list(range(SIZE)),
        "b": [x * 10 for x in range(SIZE)],
    },
)

# handle even rows
scalar_udftest_filter_even = UDFTestConfig(
    {
        "a": list(range(SIZE)),
        "b": [x * 10 if x % 2 == 0 else None for x in range(SIZE)],
    },
    "a % 2 = 0",
)


default_shuffle_config = {
    "batch_size": 1,
    "shuffle_buffer_size": 3,
    "task_shuffle_diversity": None,
}


@pytest.mark.parametrize(
    "shuffle_config",
    [
        {
            "batch_size": batch_size,
            "shuffle_buffer_size": shuffle_buffer_size,
            "task_shuffle_diversity": task_shuffle_diversity,
            "intra_applier_concurrency": intra_applier_concurrency,
        }
        for (
            batch_size,
            shuffle_buffer_size,
            task_shuffle_diversity,
            intra_applier_concurrency,
        ) in itertools.product(
            [4, 16],
            [7],
            [3],
            [1, 4],  # simple applier or multiprocessing batch applier= 4
        )
    ],
)
def test_run_ray_add_column(tmp_path: Path, shuffle_config) -> None:
    tbl = setup_table_and_udf_column(tmp_path, shuffle_config, times_ten)
    backfill_and_verify(tbl, scalar_udftest)


def test_run_ray_add_column_ifnull(tmp_path: Path) -> None:
    tbl = setup_table_and_udf_column(tmp_path, default_shuffle_config, times_ten)
    backfill_and_verify(tbl, scalar_udftest_filter_even)
    backfill_and_verify(
        tbl, UDFTestConfig(scalar_udftest.expected_recordbatch, where="b is null")
    )


def test_ray_run_add_column_filter_incremental(tmp_path: Path) -> None:
    tbl = setup_table_and_udf_column(tmp_path, default_shuffle_config, times_ten)

    backfill_and_verify(tbl, scalar_udftest_filter_even)

    # add rows divisible by 3
    scalar_udftest_filter_treys = UDFTestConfig(
        {
            "a": list(range(SIZE)),
            "b": [x * 10 if x % 3 == 0 or x % 2 == 0 else None for x in range(SIZE)],
        },
        "a % 3 = 0",
    )
    backfill_and_verify(tbl, scalar_udftest_filter_treys)

    # add odd rows
    expected = {
        "a": list(range(SIZE)),
        "b": [x * 10 for x in range(SIZE)],  # all rows covered
    }
    backfill_and_verify(tbl, UDFTestConfig(expected, where="a % 2 = 1"))


# Backfill tests with struct return types

struct_type = pa.struct([("rpad", pa.string()), ("lpad", pa.string())])


@udf(data_type=struct_type, batch_size=8, num_cpus=0.1)
def struct_udf(a: int) -> dict:  # is the output type correct?
    return {"lpad": f"{a:04d}", "rpad": f"{a}0000"[:4]}


@udf(data_type=struct_type, batch_size=8, num_cpus=0.1)
def struct_udf_batch(a: pa.Array) -> pa.Array:  # is the output type correct?
    rpad = pc.ascii_rpad(pc.cast(a, target_type="string"), 4, padding="0")
    lpad = pc.ascii_lpad(pc.cast(a, target_type="string"), 4, padding="0")
    return pc.make_struct(rpad, lpad, field_names=["rpad", "lpad"])


@udf(data_type=struct_type, batch_size=8, num_cpus=0.1)
def struct_udf_recordbatch(
    batch: pa.RecordBatch,
) -> pa.Array:  # is the output type correct?
    a = batch["a"]
    rpad = pc.ascii_rpad(pc.cast(a, target_type="string"), 4, padding="0")
    lpad = pc.ascii_lpad(pc.cast(a, target_type="string"), 4, padding="0")
    return pc.make_struct(rpad, lpad, field_names=["rpad", "lpad"])


ret_struct_udftest_complete = UDFTestConfig(
    {
        "a": list(range(SIZE)),
        "b": [{"lpad": f"{x:04d}", "rpad": f"{x}0000"[:4]} for x in range(SIZE)],
    },
)

ret_struct_udftest_filtered = UDFTestConfig(
    {
        "a": list(range(SIZE)),
        "b": [
            {"lpad": f"{x:04d}", "rpad": f"{x}0000"[:4]}
            if x % 2 == 0
            else {
                "lpad": None,
                "rpad": None,
            }  # TODO why struct of None instead of just None?
            for x in range(SIZE)
        ],
    },
    "a % 2 = 0",
)


def test_run_ray_add_column_ret_struct(tmp_path: Path) -> None:
    tbl = setup_table_and_udf_column(tmp_path, default_shuffle_config, struct_udf)
    backfill_and_verify(tbl, ret_struct_udftest_filtered)
    backfill_and_verify(tbl, ret_struct_udftest_complete)


def test_run_ray_add_column_ret_struct_batchudf(tmp_path: Path) -> None:
    tbl = setup_table_and_udf_column(tmp_path, default_shuffle_config, struct_udf_batch)
    backfill_and_verify(tbl, ret_struct_udftest_filtered)
    backfill_and_verify(tbl, ret_struct_udftest_complete)


def test_run_ray_add_column_ret_struct_recordbatchudf(tmp_path: Path) -> None:
    tbl = setup_table_and_udf_column(
        tmp_path, default_shuffle_config, struct_udf_recordbatch
    )
    backfill_and_verify(tbl, ret_struct_udftest_filtered)
    backfill_and_verify(tbl, ret_struct_udftest_complete)


def test_run_ray_add_column_ret_struct_ifnull(tmp_path: Path) -> None:
    tbl = setup_table_and_udf_column(tmp_path, default_shuffle_config, struct_udf)
    backfill_and_verify(tbl, ret_struct_udftest_filtered)
    # TODO why struct of None instead of just 'b is null'
    backfill_and_verify(
        tbl,
        UDFTestConfig(
            ret_struct_udftest_complete.expected_recordbatch,
            where="b.rpad is null and b.lpad is null",
        ),
    )


@pytest.mark.timeout(30)  # seconds
def test_run_ray_add_column_ret_struct_filtered(tmp_path: Path) -> None:
    tbl = setup_table_and_udf_column(tmp_path, default_shuffle_config, struct_udf)
    backfill_and_verify(tbl, ret_struct_udftest_filtered)
    expected = ret_struct_udftest_complete.expected_recordbatch
    backfill_and_verify(tbl, UDFTestConfig(expected, "a % 2 = 1"))


# Backfill tests with struct and array return types

vararray_type = pa.list_(pa.int64())

ret_vararray_udftest_complete = UDFTestConfig(
    {
        "a": list(range(SIZE)),
        "b": [[x] * x for x in range(SIZE)],
    },
)

ret_vararray_udftest_even = UDFTestConfig(
    {
        "a": list(range(SIZE)),
        "b": [[x] * x if x % 2 == 0 else None for x in range(SIZE)],
    },
    "a%2=0",
)


def test_run_ray_add_column_ret_vararray(tmp_path: Path) -> None:
    @udf(data_type=vararray_type, batch_size=8, num_cpus=0.1)
    def vararray_udf_scalar(a: int) -> pa.Array:  # is the output type correct?
        # [ [], [1], [2,2], [3,3,3] ... ]
        return [a] * a

    tbl = setup_table_and_udf_column(
        tmp_path, default_shuffle_config, vararray_udf_scalar
    )
    backfill_and_verify(tbl, ret_vararray_udftest_even)
    expected = ret_vararray_udftest_complete.expected_recordbatch
    backfill_and_verify(tbl, UDFTestConfig(expected, "b is null"))


def test_run_ray_add_column_ret_vararray_array(tmp_path: Path) -> None:
    @udf(data_type=vararray_type, batch_size=8, num_cpus=0.1)
    def vararray_udf(a: pa.Array) -> pa.Array:  # is the output type correct?
        # [ [], [1], [2,2], [3,3,3] ... ]
        arr = [[val] * val for val in a.to_pylist()]
        b = pa.array(arr, type=pa.list_(pa.int64()))
        return b

    tbl = setup_table_and_udf_column(tmp_path, default_shuffle_config, vararray_udf)
    backfill_and_verify(tbl, ret_vararray_udftest_even)
    expected = ret_vararray_udftest_complete.expected_recordbatch
    backfill_and_verify(tbl, UDFTestConfig(expected, "b is null"))


def test_run_ray_add_column_ret_vararray_stateful_arrays(tmp_path: Path) -> None:
    @udf(data_type=vararray_type, batch_size=8, num_cpus=0.1)
    class StatefulVararrayUDF(Callable):
        def __init__(self) -> None:
            self.state = 0

        def __call__(self, a: pa.Array) -> pa.Array:  # is the output type correct?
            # [ [], [1], [2,2], [3,3,3] ... ]
            arr = [[val] * val for val in a.to_pylist()]
            b = pa.array(arr, type=pa.list_(pa.int64()))
            return b

    tbl = setup_table_and_udf_column(
        tmp_path, default_shuffle_config, StatefulVararrayUDF()
    )
    backfill_and_verify(tbl, ret_vararray_udftest_complete)


def test_run_ray_add_column_ret_vararray_stateful_recordbatch(tmp_path: Path) -> None:
    @udf(data_type=vararray_type, batch_size=8, num_cpus=0.1)
    class BatchedStatefulVararrayUDF(Callable):
        def __init__(self) -> None:
            self.state = 0

        def __call__(
            self, batch: pa.RecordBatch
        ) -> pa.Array:  # is the output type correct?
            # [ [], [1], [2,2], [3,3,3] ... ]
            _LOG.warning(f"batch: {batch}")
            alist = batch["a"]
            arr = [[val] * val for val in alist.to_pylist()]
            b = pa.array(arr, type=pa.list_(pa.int64()))
            return b

    tbl = setup_table_and_udf_column(
        tmp_path, default_shuffle_config, BatchedStatefulVararrayUDF()
    )
    backfill_and_verify(tbl, ret_vararray_udftest_complete)


# Backfill tests with nested struct and array return types

nested_type = pa.struct([("lpad", pa.string()), ("array", pa.list_(pa.int64()))])


def test_run_ray_add_column_ret_nested(tmp_path: Path) -> None:
    @udf(data_type=nested_type, batch_size=8, num_cpus=0.1)
    def nested_udf(a: pa.Array) -> pa.Array:
        # [ { lpad:"0000", array:[] } , {lpad:"0001", array:[1]},
        #   { lpad:"0002", array:[2,2]}, ... ]

        lpad = pc.ascii_lpad(pc.cast(a, target_type="string"), 4, padding="0")
        arr = [[val] * val for val in a.to_pylist()]
        array = pa.array(arr, type=pa.list_(pa.int64()))

        return pc.make_struct(lpad, array, field_names=["lpad", "array"])

    tbl = setup_table_and_udf_column(tmp_path, default_shuffle_config, nested_udf)

    ret_nested_udftest = UDFTestConfig(
        {
            "a": list(range(SIZE)),
            "b": [{"lpad": f"{val:04d}", "array": [val] * val} for val in range(SIZE)],
        },
    )
    backfill_and_verify(tbl, ret_nested_udftest)


# Blob-type tests


def blob_table(tmp_path) -> Table:
    db = connect(tmp_path)
    schema = pa.schema(
        [
            pa.field("a", pa.int32()),
            pa.field(
                "blob", pa.large_binary(), metadata={"lance-encoding:blob": "true"}
            ),
        ]
    )
    blobs = [b"hello", b"the world"]
    tbl = pa.Table.from_pydict(
        {"a": list(range(len(blobs))), "blob": blobs}, schema=schema
    )
    tbl = db.create_table("t", tbl)
    return tbl


@udf
def work_on_udf(blob: BlobFile) -> int:
    assert isinstance(blob, BlobFile)
    return len(blob.read())


# Reload and checkpoint workflows


def test_rebackfill(tmp_path: Path) -> None:
    tbl = setup_table_and_udf_column(tmp_path, default_shuffle_config, times_ten)
    backfill_and_verify(tbl, scalar_udftest)

    tbl.drop_columns(["b"])
    tbl.add_columns({"b": times_ten})

    # should pass but b is all None
    backfill_and_verify(tbl, scalar_udftest)
