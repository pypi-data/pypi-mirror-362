from typing import TYPE_CHECKING, Any, Optional

import mlflow

from databricks.sdk import WorkspaceClient
from databricks.sdk.errors.platform import InvalidParameterValue
from databricks.sdk.service import catalog
from databricks.sdk.service.ml import (
    ExperimentAccessControlResponse,
    ExperimentPermissionLevel,
)
from databricks.sdk.service.serving import (
    ServingEndpointAccessControlResponse,
    ServingEndpointPermissionLevel,
)
from databricks.sdk.service.workspace import (
    WorkspaceObjectPermissionLevel,
)

_TRACE_METADATA_REVIEW_APP_USER = "reviewApp.userName"
_TRACE_TAG_MLFLOW_USER = "mlflow.user"

if TYPE_CHECKING:
    from databricks.rag_eval.clients.mlflow_client import MLFlowClient


def _get_custom_mlflow_client() -> "MLFlowClient":
    from databricks.rag_eval import context

    @context.eval_context
    def getter():
        return context.get_context().build_mlflow_client()

    return getter()


def log_trace_to_experiment(
    trace: mlflow.entities.Trace, experiment_id: str, run_id: Optional[str]
) -> mlflow.entities.Trace:
    # Only clone the trace if it's not already associated with the same experiment.
    if (
        not trace.info.trace_location
        or not trace.info.trace_location.mlflow_experiment
        or trace.info.trace_location.mlflow_experiment.experiment_id != experiment_id
    ):
        # Make a copy of the trace before modifying it.
        trace = trace.from_dict(trace.to_dict())
        trace.info.trace_location = mlflow.entities.TraceLocation(
            type=mlflow.entities.TraceLocationType.MLFLOW_EXPERIMENT,
            mlflow_experiment=mlflow.entities.MlflowExperimentLocation(
                experiment_id=experiment_id,
            ),
        )
        mlflow_client = mlflow.MlflowClient()
        new_trace_id = mlflow_client._log_trace(trace)
        trace.info.trace_id = new_trace_id

    if run_id:
        # Associate the trace with the given run.
        _get_custom_mlflow_client().link_traces_to_run(
            run_id=run_id,
            trace_ids=[trace.info.trace_id],
        )

    return trace


def _has_edit_permission_in_experiment(
    user: str, acls: list[ExperimentAccessControlResponse]
) -> bool:
    """Returns True if the user has edit permissions for an experiment."""
    for acl in acls:
        if user in (acl.user_name, acl.group_name, acl.service_principal_name):
            for permission in acl.all_permissions:
                if permission.permission_level in (
                    ExperimentPermissionLevel.CAN_EDIT,
                    ExperimentPermissionLevel.CAN_MANAGE,
                ):
                    return True
    return False


def add_users_to_experiment(users: list[str], experiment_id: str) -> None:
    from databricks.agents.permissions import _update_permissions_on_experiment

    print(
        f"Users {users} will be given WRITE access to the experiment "
        f"with id '{experiment_id}'"
    )
    # Filter out users that already have edit permissions on the experiment.
    w = WorkspaceClient()
    experiment_type = "experiments"
    try:
        acls = w.experiments.get_permissions(experiment_id).access_control_list
    except InvalidParameterValue:
        # If the experiment is associated with a notebook, get the permissions from the notebook.
        acls = w.workspace.get_permissions(
            "notebooks", experiment_id
        ).access_control_list
        experiment_type = "notebooks"

    users = [u for u in users if not _has_edit_permission_in_experiment(u, acls)]

    _update_permissions_on_experiment(
        [experiment_id],
        users,
        experiment_type,
        WorkspaceObjectPermissionLevel.CAN_EDIT,
    )


def add_users_to_dataset(user_emails: list[str], dataset_name: str) -> None:
    """Grants read access to the given users on the specified dataset."""
    print(
        f"Users {user_emails} will be given a SELECT privilege to the dataset '{dataset_name}'"
    )
    w = WorkspaceClient()
    w.grants.update(
        securable_type=catalog.SecurableType.TABLE.value,
        full_name=dataset_name,
        changes=[
            catalog.PermissionsChange(
                principal=user_email,
                add=[catalog.Privilege.SELECT],
            )
            for user_email in user_emails
        ],
    )


def _has_query_permission_in_serving(
    user: str, acls: list[ServingEndpointAccessControlResponse]
) -> bool:
    """Returns True if the user has query permissions for a serving endpoint."""
    for acl in acls:
        if user in (acl.user_name, acl.group_name, acl.service_principal_name):
            for permission in acl.all_permissions:
                if permission.permission_level in (
                    ServingEndpointPermissionLevel.CAN_QUERY,
                    ServingEndpointPermissionLevel.CAN_MANAGE,
                ):
                    return True
    return False


def add_users_to_serving_endpoint(users: list[str], endpoint_name: str) -> None:
    from databricks.agents.permissions import _update_permissions_on_endpoint

    print(
        f"Users {users} will be given QUERY access to the model "
        f"serving endpoint '{endpoint_name}'"
    )
    w = WorkspaceClient()
    endpoint = w.serving_endpoints.get(endpoint_name)
    if not endpoint.id:
        # This endpoint is part of the FM API, so we can't modify its permissions.
        return

    # Filter out users that already have query permissions on the endpoint.
    acls = w.serving_endpoints.get_permissions(endpoint.id).access_control_list
    users = [u for u in users if not _has_query_permission_in_serving(u, acls)]

    _update_permissions_on_endpoint(
        endpoint.id, users, ServingEndpointPermissionLevel.CAN_QUERY
    )


def assessments_to_expectations_dict(
    assessments: list[mlflow.entities.Assessment],
) -> dict:
    """Converts a list of assessments to a dictionary of expectations."""
    expectations: dict[str, Any] = {}
    for assessment in assessments:
        if assessment.expectation:
            expectations[assessment.name] = assessment.expectation.value
    return expectations


def extract_user_email_from_trace(trace: mlflow.entities.Trace) -> Optional[str]:
    """Extracts the email of the creator from the trace."""
    # Obtain the creator of the trace.
    return trace.info.trace_metadata.get(
        _TRACE_METADATA_REVIEW_APP_USER
    ) or trace.info.tags.get(_TRACE_TAG_MLFLOW_USER)
