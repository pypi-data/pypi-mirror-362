from typing import Optional

import requests
from mlflow.genai.scheduled_scorers import ScorerScheduleConfig
from mlflow.genai.scorers.base import Scorer

from databricks.rag_eval import context
from databricks.rag_eval.monitoring.api import _get_managed_evals_client


@context.eval_context
def add_scheduled_scorer(
    experiment_id: str,
    scheduled_scorer_name: str,
    scorer: Scorer,
    sample_rate: float,
    filter_string: Optional[str] = None,
) -> ScorerScheduleConfig:
    """
    Add a scheduled scorer to automatically monitor traces in an MLflow experiment.

    This function configures a scorer function to run automatically on traces logged to the
    specified experiment. The scorer will evaluate a sample of traces based on the sampling rate
    and any filter criteria. Assessments are displayed in the Traces tab of the MLflow experiment.

    Args:
        experiment_id: The ID of the MLflow experiment to monitor. If None, uses the
            currently active experiment.
        scheduled_scorer_name: The name for this scheduled scorer within the experiment.
            We recommend using the scorer's name (e.g., scorer.name) for consistency.
        scorer: The scorer function to execute on sampled traces. Must be either a
            built-in scorer or a function decorated with @scorer. Subclasses of Scorer
            are not supported.
        sample_rate: The fraction of traces to evaluate, between 0.0 and 1.0. For example,
            0.3 means 30% of traces will be randomly selected for evaluation.
        filter_string: An optional MLflow search_traces compatible filter string. Only
            traces matching this filter will be considered for evaluation. If None,
            all traces in the experiment are eligible for sampling.

            Note: This parameter is not currently supported and will be added in a future release.

    Returns:
        A ScorerScheduleConfig object representing the configured scheduled scorer.
    """
    client = _get_managed_evals_client()

    scorer_config = ScorerScheduleConfig(
        scorer=scorer,
        scheduled_scorer_name=scheduled_scorer_name,
        sample_rate=sample_rate,
        filter_string=filter_string,
    )

    # Try to get existing scorers, handle case where none exist
    try:
        existing_scorer_configs = client.get_scheduled_scorers(
            experiment_id=experiment_id
        )
    except requests.HTTPError as e:
        if e.response.status_code == 404:
            # No scheduled scorers exist yet, start with empty list
            client.create_scheduled_scorers(
                experiment_id=experiment_id,
                scheduled_scorers=[scorer_config],
            )
            return scorer_config
        raise

    existing_names = [
        config.scheduled_scorer_name for config in existing_scorer_configs
    ]
    if scheduled_scorer_name in existing_names:
        raise ValueError(
            f"A scheduled scorer with name '{scheduled_scorer_name}' already exists. "
            "Use update_scheduled_scorer() to modify it or choose a different name."
        )

    new_scorer_configs = existing_scorer_configs + [scorer_config]

    client.update_scheduled_scorers(
        experiment_id=experiment_id,
        scheduled_scorers=new_scorer_configs,
        update_mask="scheduled_scorers.scorers",
    )

    return scorer_config


@context.eval_context
def update_scheduled_scorer(
    experiment_id: str,
    scheduled_scorer_name: str,
    scorer: Optional[Scorer] = None,
    sample_rate: Optional[float] = None,
    filter_string: Optional[str] = None,
) -> ScorerScheduleConfig:
    """
    Update an existing scheduled scorer configuration.

    This function modifies the configuration of an existing scheduled scorer, allowing you
    to change the scorer function, sampling rate, or filter criteria. Only the provided
    parameters will be updated; omitted parameters will retain their current values.
    The scorer will continue to run automatically with the new configuration.

    Args:
        experiment_id: The ID of the MLflow experiment containing the scheduled scorer.
            If None, uses the currently active experiment.
        scheduled_scorer_name: The name of the existing scheduled scorer to update. Must match
            the name used when the scorer was originally added. We recommend using the
            scorer's name (e.g., scorer.name) for consistency.
        scorer: The new scorer function to execute on sampled traces. Must be either
            a built-in scorer or a function decorated with @scorer. If None, the
            current scorer function will be retained.
        sample_rate: The new fraction of traces to evaluate, between 0.0 and 1.0.
            If None, the current sample rate will be retained.
        filter_string: The new MLflow search_traces compatible filter string. If None,
            the current filter string will be retained. Pass an empty string to remove
            the filter entirely.

            Note: This parameter is not currently supported and will be added in a future release.

    Returns:
        A ScorerScheduleConfig object representing the updated scheduled scorer configuration.
    """
    client = _get_managed_evals_client()

    existing_scorer_configs = client.get_scheduled_scorers(experiment_id=experiment_id)

    scorer_to_update = None

    for existing_config in existing_scorer_configs:
        if existing_config.scheduled_scorer_name == scheduled_scorer_name:
            scorer_to_update = existing_config
            break

    if scorer_to_update is None:
        raise ValueError(
            f"No scheduled scorer found with name '{scheduled_scorer_name}'. "
            "Use add_scheduled_scorer() to create a new scorer."
        )

    scorer_to_update.scorer = scorer
    scorer_to_update.sample_rate = sample_rate
    scorer_to_update.filter_string = filter_string

    client.update_scheduled_scorers(
        experiment_id=experiment_id,
        scheduled_scorers=existing_scorer_configs,
        update_mask="scheduled_scorers.scorers",
    )

    return scorer_to_update


@context.eval_context
def delete_scheduled_scorer(
    experiment_id: str,
    scheduled_scorer_name: str,
) -> None:
    """
    Delete a scheduled scorer from an MLflow experiment.

    This function removes a scheduled scorer configuration, stopping automatic evaluation
    of traces. Existing Assessments will remain in the Traces tab of the MLflow
    experiment, but no new evaluations will be performed.

    Args:
        experiment_id: The ID of the MLflow experiment containing the scheduled scorer.
            If None, uses the currently active experiment.
        scheduled_scorer_name: The name of the scheduled scorer to delete. Must match the name
            used when the scorer was originally added.
    """
    client = _get_managed_evals_client()

    existing_scorer_configs = client.get_scheduled_scorers(experiment_id=experiment_id)

    updated_scorer_configs = [
        c
        for c in existing_scorer_configs
        if c.scheduled_scorer_name != scheduled_scorer_name
    ]

    if len(updated_scorer_configs) == len(existing_scorer_configs):
        raise ValueError(
            f"No scheduled scorer found with name '{scheduled_scorer_name}'"
        )

    client.update_scheduled_scorers(
        experiment_id=experiment_id,
        scheduled_scorers=updated_scorer_configs,
        update_mask="scheduled_scorers.scorers",
    )


@context.eval_context
def get_scheduled_scorer(
    experiment_id: str,
    scheduled_scorer_name: str,
) -> ScorerScheduleConfig:
    """
    Retrieve the configuration of a specific scheduled scorer.

    This function returns the current configuration of a scheduled scorer, including
    its scorer function, sampling rate, and filter criteria.

    Args:
        experiment_id: The ID of the MLflow experiment containing the scheduled scorer.
            If None, uses the currently active experiment.
        scheduled_scorer_name: The name of the scheduled scorer to retrieve.

    Returns:
        A ScorerScheduleConfig object containing the current configuration of the specified
        scheduled scorer.
    """
    client = _get_managed_evals_client()

    existing_scorer_configs = client.get_scheduled_scorers(experiment_id=experiment_id)

    for config in existing_scorer_configs:
        if config.scheduled_scorer_name == scheduled_scorer_name:
            return config

    raise ValueError(f"No scheduled scorer found with name '{scheduled_scorer_name}'")


@context.eval_context
def list_scheduled_scorers(
    experiment_id: str,
) -> list[ScorerScheduleConfig]:
    """
    List all scheduled scorers for an experiment.

    This function returns all scheduled scorers configured for the specified experiment,
    or for the current active experiment if no experiment ID is provided.

    Args:
        experiment_id: The ID of the MLflow experiment to list scheduled scorers for.
            If None, uses the currently active experiment.

    Returns:
        A list of ScheduledScorerConfig objects representing all scheduled scorers configured
        for the specified experiment.
    """
    client = _get_managed_evals_client()

    return client.get_scheduled_scorers(experiment_id=experiment_id)


@context.eval_context
def set_scheduled_scorers(
    experiment_id: str,
    scheduled_scorers: list[ScorerScheduleConfig],
) -> None:
    """
    Replace all scheduled scorers for an experiment with the provided list.

    This function removes all existing scheduled scorers for the specified experiment
    and replaces them with the new list. This is useful for batch configuration updates
    or when you want to ensure only specific scorers are active.

    Args:
        experiment_id: The ID of the MLflow experiment to configure. If None, uses the
            currently active experiment.
        scheduled_scorers: A list of ScheduledScorerConfig objects to set as the complete
            set of scheduled scorers for the experiment. Any existing scheduled scorers
            not in this list will be removed.
    """
    client = _get_managed_evals_client()

    # Check if scheduled scorers already exist
    try:
        _existing_scorer_configs = client.get_scheduled_scorers(
            experiment_id=experiment_id
        )
        # If we get here, scorers exist, so we can update them
        client.update_scheduled_scorers(
            experiment_id=experiment_id,
            scheduled_scorers=scheduled_scorers,
            update_mask="scheduled_scorers.scorers",
        )
    except requests.HTTPError as e:
        if e.response.status_code == 404:
            # No scheduled scorers exist yet, create them
            client.create_scheduled_scorers(
                experiment_id=experiment_id,
                scheduled_scorers=scheduled_scorers,
            )
        else:
            raise
