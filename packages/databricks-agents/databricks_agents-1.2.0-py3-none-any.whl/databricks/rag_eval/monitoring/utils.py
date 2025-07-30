import hashlib
import re
import time

import mlflow
from mlflow import entities as mlflow_entities
from mlflow.tracking import fluent

from databricks.agents.utils.mlflow_utils import get_workspace_url
from databricks.rag_eval.utils import uc_utils


def get_monitoring_page_url(experiment_id: str) -> str:
    """Get the monitoring page URL.

    Args:
        experiment_id (str): id of the experiment

    Returns:
        str: the monitoring page URL
    """
    return (
        f"{get_workspace_url()}/ml/experiments/{experiment_id}?compareRunsMode=TRACES"
    )


def get_databricks_mlflow_experiment(
    *,
    experiment_id: str | None = None,
    experiment_name: str | None = None,
) -> mlflow_entities.Experiment:
    if experiment_id:
        return mlflow.get_experiment(experiment_id=experiment_id)

    if experiment_name:
        exp = mlflow.get_experiment_by_name(name=experiment_name)
        if exp is None:
            raise ValueError(
                f"Experiment with name '{experiment_name}' does not exist. "
                "Please create the experiment before using it."
            )

    # Infer the experiment ID from the current environment.
    try:
        experiment_id = fluent._get_experiment_id()
    except Exception:
        raise ValueError(
            "Please provide an experiment_name or run this code within an active experiment."
        )

    if experiment_id == mlflow.tracking.default_experiment.DEFAULT_EXPERIMENT_ID:
        raise ValueError

    return mlflow.get_experiment(experiment_id=str(experiment_id))


def simple_hex_hash(s: str) -> str:
    """
    Generate a hex hash string of length 6 for the given input string.

    Args:
        s (str): The input string.

    Returns:
        str: A 6-character long hex hash.
    """
    # Create an MD5 hash object with the encoded input string
    hash_object = hashlib.md5(s.encode("utf-8"))

    # Get the full hex digest and then take the first 6 characters
    return hash_object.hexdigest()[:6]


def create_checkpoint_table_entity_name(experiment_name: str) -> str:
    """Create a checkpoint table entity name based on the experiment name and current time.

    Example: "test_experiment_name" -> "ckpt_test_experiment_name_a1b2c3"

    Args:
        experiment_name (str): Name of the experiment.

    Returns:
        str: The generated checkpoint table entity name.
    """

    hash = simple_hex_hash(f"{experiment_name}_{time.time()}")
    prefix = "ckpt"
    # Subtract 8 from limit to provide extra room for `monitor_` prefix when building endpoint name.
    # This allows the endpoint name to also avoid conflicts thanks to the hash.
    max_name_chars = uc_utils.MAX_UC_ENTITY_NAME_LEN - len(hash) - len(prefix) - 2 - 8
    processed_experiment_name = re.sub(r"[./ ]", "_", experiment_name)

    return f"{prefix}_{processed_experiment_name[:max_name_chars]}_{hash}"
