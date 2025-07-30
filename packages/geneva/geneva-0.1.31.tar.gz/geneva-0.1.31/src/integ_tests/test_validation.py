# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright The Geneva Authors

import pytest

from geneva.runners.ray.raycluster import RayCluster, _WorkerGroupSpec


def test_service_account_does_not_exist() -> None:
    cluster = RayCluster(
        name="not-used",
        namespace="geneva",
        # allocate at least a single worker so the test runs faster
        # that we save time on waiting for the actor to start
        worker_groups=[
            _WorkerGroupSpec(
                name="worker", min_replicas=1, service_account="does-not-exist"
            )
        ],
    )
    with pytest.raises(
        ValueError, match="Service account does-not-exist does not exist"
    ):
        cluster._validate()


def test_service_account_not_enough_permission(
    k8s_temp_service_account: str,
) -> None:
    # with strict access review, we should get an error about lack of permission
    cluster = RayCluster(
        name="not-used",
        namespace="geneva",
        # allocate at least a single worker so the test runs faster
        # that we save time on waiting for the actor to start
        worker_groups=[
            _WorkerGroupSpec(
                name="worker",
                min_replicas=1,
                service_account=k8s_temp_service_account,
            )
        ],
        strict_access_review=True,
    )
    with pytest.raises(
        ValueError,
        match=f"Service account {k8s_temp_service_account} does not"
        " have the required permission:",
    ):
        cluster._validate()

    # with strict access review disabled, we should still get the same
    # error because we have permission to create local subject access
    # review and the service account does not have enough permission
    cluster = RayCluster(
        name="not-used",
        namespace="geneva",
        # allocate at least a single worker so the test runs faster
        # that we save time on waiting for the actor to start
        worker_groups=[
            _WorkerGroupSpec(
                name="worker",
                min_replicas=1,
                service_account=k8s_temp_service_account,
            )
        ],
        strict_access_review=False,
    )
    with pytest.raises(
        ValueError,
        match=f"Service account {k8s_temp_service_account} does not"
        " have the required permission:",
    ):
        cluster._validate()


def test_service_account_is_valid(
    geneva_k8s_service_account: str,
) -> None:
    cluster = RayCluster(
        name="not-used",
        namespace="geneva",
        # allocate at least a single worker so the test runs faster
        # that we save time on waiting for the actor to start
        worker_groups=[
            _WorkerGroupSpec(
                name="worker",
                min_replicas=1,
                service_account=geneva_k8s_service_account,
            )
        ],
    )
    cluster._validate()
