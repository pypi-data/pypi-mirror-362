# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright The Geneva Authors

import itertools
import logging
from collections.abc import Callable
from pathlib import Path
from typing import Any, NamedTuple

import lance
import pandas as pd
import pyarrow as pa
import pyarrow.compute as pc
import pytest
from lance.blob import BlobFile

import geneva
from geneva import LanceCheckpointStore, connect, udf
from geneva.apply.multiprocess import MultiProcessBatchApplier
from geneva.apply.simple import SimpleApplier
from geneva.table import Table, TableReference

_LOG = logging.getLogger(__name__)
_LOG.setLevel(logging.DEBUG)

SIZE = 17  # was 256

try:
    import ray

    from geneva.runners.ray.pipeline import _simulate_write_failure, run_ray_add_column
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


@pytest.fixture
def basic_dataset(tbl_path: Path) -> lance.dataset:
    return make_new_ds_a(tbl_path)


@pytest.fixture
def geneva_init_table(tmp_path, basic_dataset) -> Table:
    db = geneva.connect(str(tmp_path))
    tbl = db.open_table("foo")
    return tbl


@pytest.fixture
def tbl_ref(tmp_path) -> TableReference:
    return TableReference(db_uri=str(tmp_path), table_name="foo", version=None)


@pytest.fixture
def ckp_store(tmp_path) -> LanceCheckpointStore:
    return LanceCheckpointStore(str(tmp_path / "ckp"))


def make_new_ds_a(tbl_path: Path) -> lance.dataset:
    # create initial dataset with only column 'a'
    data = {"a": pa.array(range(SIZE))}
    tbl = pa.Table.from_pydict(data)
    ds = lance.write_dataset(tbl, tbl_path, max_rows_per_file=32)
    return ds


def make_new_ds(tbl_path: Path, fn) -> None:
    ds = make_new_ds_a(tbl_path)

    # then add column 'b' using merge.  This is a separate commit from data
    # commits to keep column 'a' as a separate set of physical files from 'b'
    # which enables a separate commit from distributed execution to only
    # update 'b' with an efficient file replacement operation.
    new_frags = []
    new_schema = None
    for frag in ds.get_fragments():
        new_fragment, new_schema = frag.merge_columns(fn, columns=["a"])
        new_frags.append(new_fragment)

    assert new_schema is not None
    merge = lance.LanceOperation.Merge(new_frags, new_schema)
    lance.LanceDataset.commit(tbl_path, merge, read_version=ds.version)


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
    job_id = tbl.backfill("b", where=testcfg.where)
    _LOG.info(f"completed backfill job {job_id}, now on version {tbl.version}")
    _LOG.info(
        f"actual={tbl.to_arrow().to_pydict()} expected={testcfg.expected_recordbatch}"
    )
    assert tbl.to_arrow().to_pydict() == testcfg.expected_recordbatch

    _LOG.info(f"Checking job history for {job_id}")
    _LOG.info(f"{tbl._conn._history.jobs_table.to_arrow().to_pylist()}")

    hist = tbl._conn._history
    jr = hist.get(job_id)[0]
    assert jr.status == "DONE"
    assert jr.object_ref is not None
    assert jr.table_name == tbl.name
    assert jr.column_name == "b"
    assert jr.launched_at is not None
    assert jr.completed_at is not None


# UDF argument validation tests


@udf(data_type=pa.int32())
def recordbatch_udf(batch: pa.RecordBatch) -> pa.Array:
    return batch["a"]


def test_recordbatch_bad_inputs(tmp_path) -> None:
    # record batch udfs don't take input_columns args
    with pytest.raises(ValueError, match="please specify data_type"):

        @udf(input_columns=["a"])
        def recordbatch_bad(batch: pa.RecordBatch) -> pa.Array:
            return batch["a"]

    # record batch udfs need output data_type arg
    with pytest.raises(ValueError, match="please specify data_type"):

        @udf
        def recordbatch_bad(batch: pa.RecordBatch) -> pa.Array:
            return batch["a"]

    # set good udf, but have bad overrides
    tbl = setup_table_and_udf_column(tmp_path, default_shuffle_config, recordbatch_udf)

    # record batch udfs cannot override input cols
    with pytest.raises(
        ValueError, match="RecordBatch input UDF must not declare any input column"
    ):
        tbl.backfill("b", input_columns=["a"])

    # override recordbatch udfs can't take input cols
    with pytest.raises(
        ValueError, match="RecordBatch input UDF must not declare any input column"
    ):
        tbl.backfill("b", udf=recordbatch_udf, input_columns=["a"])

    # override backfill pass
    tbl.backfill("b", udf=recordbatch_udf)


def test_invalid_column(tmp_path) -> None:
    tbl = setup_table_and_udf_column(tmp_path, default_shuffle_config, recordbatch_udf)

    # input cols arg
    with pytest.raises(ValueError, match="Use add_columns"):
        tbl.backfill("c", udf=recordbatch_udf)


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


@pytest.mark.parametrize(
    "batch_applier", [SimpleApplier(), MultiProcessBatchApplier(num_processes=4)]
)
def test_run_ray_add_column_write_fault(
    tbl_path, tbl_ref, ckp_store, batch_applier
) -> None:  # noqa: PT019
    make_new_ds(tbl_path, int32_return_none)

    with _simulate_write_failure(True):
        run_ray_add_column(
            tbl_ref,
            ["a"],
            {"b": times_ten},
            checkpoint_store=ckp_store,
            batch_applier=batch_applier,
        )

    ds = lance.dataset(tbl_path)
    assert ds.to_table().to_pydict() == scalar_udftest.expected_recordbatch


def test_run_ray_add_column_with_deletes(tbl_path, tbl_ref, ckp_store) -> None:  # noqa: PT019
    make_new_ds(tbl_path, int32_return_none)
    ds = lance.dataset(tbl_path)
    ds.delete("a % 2 == 1")

    run_ray_add_column(tbl_ref, ["a"], {"b": times_ten}, checkpoint_store=ckp_store)

    ds = lance.dataset(tbl_path)
    assert ds.to_table().to_pydict() == {
        "a": list(range(0, SIZE, 2)),
        "b": [x * 10 for x in range(0, SIZE, 2)],
    }


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


# Other tests


def test_relative_path(tmp_path: Path, monkeypatch) -> None:
    # Make sure this ray instance uses the tmp_path as CURDIR
    ray.shutdown()
    monkeypatch.chdir(tmp_path)

    db = geneva.connect("./db")

    # create a basic table
    tbl = pa.Table.from_pydict({"id": [1, 2, 3, 4, 5, 6]})
    table = db.create_table("table1", tbl)

    @udf(data_type=pa.int64())
    def double_id(id: int):  # noqa A002
        return id * 2

    table.add_columns(
        {"id2": double_id},
    )

    schema = table.schema
    field = schema.field("id2")
    assert field.metadata[b"virtual_column.udf_name"] == b"double_id"

    # At this time, "id2" is a null column
    assert table.to_arrow().combine_chunks() == pa.Table.from_pydict(
        {"id": [1, 2, 3, 4, 5, 6], "id2": [None] * 6},
        schema=pa.schema(
            [
                pa.field("id", pa.int64()),
                pa.field("id2", pa.int64(), True),
            ]
        ),
    )

    # uses local ray to execute UDF and populate "id2"
    table.backfill("id2")

    df = table.to_arrow().to_pandas()
    assert df.equals(
        pd.DataFrame({"id": [1, 2, 3, 4, 5, 6], "id2": [2, 4, 6, 8, 10, 12]})
    )


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


def test_udf_with_blob_column(tmp_path: Path) -> None:
    tbl = blob_table(tmp_path)
    tbl.add_columns({"len": work_on_udf})
    tbl.backfill("len", input_columns=["blob"])
    vals = tbl.to_arrow()
    assert vals["len"].to_pylist() == [5, 9]


def test_udf_with_blob_column_filtered(tmp_path: Path) -> None:
    tbl = blob_table(tmp_path)
    tbl.add_columns({"len": work_on_udf})
    tbl.backfill(
        "len",
        where="a%2=0",
    )
    vals = tbl.to_arrow()
    assert vals["len"].to_pylist() == [5, None]


@pytest.mark.skip(reason="binary literal not yet implemented?")
def test_udf_with_blob_column_filtered_binaryliteral(tmp_path: Path) -> None:
    tbl = blob_table(tmp_path)
    tbl.add_columns({"len": work_on_udf})
    tbl.backfill(
        "len",
        where="blob = X'hello'",
    )
    vals = tbl.to_arrow()
    assert vals["len"].to_pylist() == [5, None]


def test_udf_generates_blob_output(tmp_path: Path) -> None:
    """Test UDF that generates Lance blob outputs from scalar inputs."""

    @udf(data_type=pa.large_binary(), field_metadata={"lance-encoding:blob": "true"})
    def generate_blob(text: str, multiplier: int) -> bytes:
        """UDF that generates blob data by repeating text."""
        return (text * multiplier).encode("utf-8")

    # Create database and input table
    db = connect(tmp_path)
    input_data = pa.table({"text": ["hello", "world", "test"], "multiplier": [2, 3, 1]})
    tbl = db.create_table("input_table", input_data)

    # Add blob column with proper metadata
    tbl.add_columns({"blob_output": generate_blob})
    _LOG.info(f"schema: {tbl.schema}")
    # Verify blob metadata is present
    blob_field = tbl.schema.field("blob_output")
    assert blob_field.metadata[b"lance-encoding:blob"] == b"true"

    # Execute backfill to generate blob data
    tbl.backfill("blob_output", input_columns=["text", "multiplier"])

    # Verify results
    tbl = db.open_table("input_table")
    result = tbl.to_arrow()
    expected_blobs = [
        {"position": 0, "size": 10},
        {"position": 64, "size": 15},
        {"position": 128, "size": 4},
    ]
    expected_blob_values = [
        b"hellohello",  # "hello" * 2
        b"worldworldworld",  # "world" * 3
        b"test",  # "test" * 1
    ]
    _LOG.info(f"result: {result}")

    assert result["text"].to_pylist() == ["hello", "world", "test"]
    assert result["multiplier"].to_pylist() == [2, 3, 1]
    assert result["blob_output"].to_pylist() == expected_blobs

    # Verify blob files' content - have to go to dataset api
    from lance import dataset as lance_dataset

    ds = lance_dataset(tbl._uri)
    blob_files = ds.take_blobs("blob_output", indices=[0, 1, 2])
    assert len(blob_files) == 3
    blob_values = [blob.read() for blob in blob_files]
    assert blob_values == expected_blob_values


def test_udf_generates_blob_from_array_input(tmp_path: Path) -> None:
    """Test UDF that generates Lance blob outputs from array inputs."""

    @udf(data_type=pa.large_binary(), field_metadata={"lance-encoding:blob": "true"})
    def serialize_array(values: pa.Array) -> bytes:
        """UDF that serializes an array into blob data."""
        import pickle

        _LOG.info(f"values ({type(values)}): {values}")
        return pickle.dumps(values)

    # Create database and input table with array column
    db = connect(tmp_path)
    array_data = [[1, 2, 3], [4, 5, 6, 7], [8, 9]]
    input_data = pa.table({"id": [1, 2, 3], "values": array_data})
    tbl = db.create_table("array_table", input_data)

    # Add blob column with proper metadata
    tbl.add_columns({"serialized_blob": serialize_array})
    # Verify blob metadata
    blob_field = tbl.schema.field("serialized_blob")
    assert blob_field.metadata[b"lance-encoding:blob"] == b"true"

    # Execute backfill
    tbl.backfill("serialized_blob", input_columns=["values"])

    # Verify results by deserializing - have to go to dataset api
    from lance import dataset as lance_dataset

    ds = lance_dataset(tbl._uri)
    blob_files = ds.take_blobs("serialized_blob", indices=[0, 1, 2])
    assert len(blob_files) == 3
    blob_values = [blob.read() for blob in blob_files]
    for i, blob_data in enumerate(blob_values):
        import pickle

        deserialized = pickle.loads(blob_data)
        assert deserialized == array_data[i]


def test_udf_generates_blob_from_recordbatch(tmp_path: Path) -> None:
    """Test RecordBatch UDF that generates Lance blob outputs."""

    @udf(data_type=pa.large_binary(), field_metadata={"lance-encoding:blob": "true"})
    def batch_to_blob(batch: pa.RecordBatch) -> pa.Array:
        """UDF that converts RecordBatch rows to blob data."""
        import json

        blobs = []
        for i in range(batch.num_rows):
            row_dict = {
                col_name: batch.column(j)[i].as_py()
                for j, col_name in enumerate(batch.column_names)
            }
            blob_data = json.dumps(row_dict, sort_keys=True).encode("utf-8")
            blobs.append(blob_data)
        return pa.array(blobs, type=pa.large_binary())

    # Create database and input table
    db = connect(tmp_path)
    input_data = pa.table(
        {
            "name": ["Alice", "Bob", "Charlie"],
            "age": [25, 30, 35],
            "score": [95.5, 87.2, 92.8],
        }
    )
    tbl = db.create_table("people_table", input_data)

    # Add blob column
    tbl.add_columns({"row_blob": batch_to_blob})

    # Verify blob metadata
    blob_field = tbl.schema.field("row_blob")
    assert blob_field.metadata[b"lance-encoding:blob"] == b"true"

    # Execute backfill
    tbl.backfill("row_blob")

    # Verify results
    result = tbl.to_arrow()

    # Verify blob files' content - have to go to dataset api
    from lance import dataset as lance_dataset

    ds = lance_dataset(tbl._uri)
    blob_files = ds.take_blobs("row_blob", indices=[0, 1, 2])
    assert len(blob_files) == 3
    blob_values = [blob.read() for blob in blob_files]
    for i, blob_data in enumerate(blob_values):
        import json

        row_dict = json.loads(blob_data.decode("utf-8"))

        # Verify the serialized data matches original
        assert row_dict["name"] == result["name"][i].as_py()
        assert row_dict["age"] == result["age"][i].as_py()
        assert abs(row_dict["score"] - result["score"][i].as_py()) < 0.001
