# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright The Geneva Authors

import contextlib
import datetime
import logging
import random
import uuid
import warnings
from collections.abc import Generator

import kubernetes
import pytest

from geneva.config import override_config_kv
from geneva.runners.ray._mgr import ray_cluster
from geneva.runners.ray.raycluster import _HeadGroupSpec, _WorkerGroupSpec

kubernetes.config.load_kube_config()

logging.basicConfig(level=logging.INFO)
# integ test specific config overrides
override_config_kv(
    {
        "uploader.upload_dir": "gs://geneva-integ-test/zips",
        "job.checkpoint.mode": "object_store",
        "job.checkpoint.object_store.path": "gs://geneva-integ-test/checkpoints",
    }
)
# it's okay, we are in a test
warnings.filterwarnings(
    "ignore", "Using port forwarding for Ray cluster is not recommended for production"
)


@pytest.fixture(autouse=True, scope="session")
def k8s_core_api() -> kubernetes.client.CoreV1Api:
    """
    This fixture is used to create a CoreV1Api object for the test session.
    """
    return kubernetes.client.CoreV1Api()


@pytest.fixture(autouse=True)
def k8s_temp_service_account(
    k8s_core_api: kubernetes.client.CoreV1Api,
) -> Generator[str, None, None]:
    name = f"geneva-test-{uuid.uuid4().hex}"
    k8s_core_api.create_namespaced_service_account(
        namespace="geneva",
        body={
            "apiVersion": "v1",
            "kind": "ServiceAccount",
            "metadata": {
                "name": name,
                "namespace": "geneva",
            },
        },
    )
    yield name
    k8s_core_api.delete_namespaced_service_account(
        name=name,
        namespace="geneva",
        body=kubernetes.client.V1DeleteOptions(),
    )


@pytest.fixture(autouse=True, scope="session")
def geneva_k8s_service_account() -> str:
    """
    A preconfigured service account for the test session.
    This service account should have all the permissions needed to run the tests.
    """
    return "geneva-integ-test"


@pytest.fixture(autouse=True, scope="session")
def geneva_test_bucket() -> str:
    """
    A preconfigured service account for the test session.
    This service account should have all the permissions needed to run the tests.
    """
    return "gs://geneva-integ-test/data"


@pytest.fixture(autouse=True)
def standard_cluster(
    geneva_k8s_service_account: str,
) -> contextlib.AbstractContextManager:
    cluster_name = "geneva-integ-test"
    cluster_name += f"-{datetime.datetime.now().strftime('%Y-%m-%d-%H-%M')}"
    cluster_name += f"-{random.randint(0, 10000)}"

    return ray_cluster(
        name=cluster_name,
        namespace="geneva",
        use_portforwarding=True,
        head_group=_HeadGroupSpec(
            service_account=geneva_k8s_service_account,
            num_cpus=1,
            memory=2 * 1024**3,
        ),
        # allocate at least a single worker so the test runs faster
        # that we save time on waiting for the actor to start
        worker_groups=[
            _WorkerGroupSpec(
                name="worker",
                min_replicas=1,
                service_account=geneva_k8s_service_account,
                num_cpus=2,
                memory=4 * 1024**3,
            )
        ],
    )
