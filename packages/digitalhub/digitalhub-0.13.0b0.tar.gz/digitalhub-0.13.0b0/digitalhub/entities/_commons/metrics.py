# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import Any, Union

from pydantic import BaseModel, ValidationError

MetricType = Union[float, int, list[Union[float, int]]]


class Metric(BaseModel):
    """
    Metric.
    """

    value: MetricType


def validate_metric_value(value: Any) -> MetricType:
    """
    Validate metric value.

    Parameters
    ----------
    value : Any
        The value to validate.

    Returns
    -------
    MetricType
        The validated value.
    """
    try:
        return Metric(value=value).value
    except ValidationError as e:
        raise ValueError("Invalid metric value. Must be a list of floats or ints or a float or an int.") from e


def set_metrics(
    metrics: dict[str, MetricType],
    key: str,
    value: Any,
    overwrite: bool,
    single_value: bool,
) -> dict[str, MetricType]:
    """
    Set metric value.

    Parameters
    ----------
    metrics : dict[str, MetricType]
        The metrics dictionary.
    key : str
        The key of the entity.
    value : Any
        The value to set.
    overwrite : bool
        Whether to overwrite the metric.

    Returns
    -------
    dict[str, MetricType]
        The metrics dictionary.
    """
    if isinstance(value, list):
        return handle_metric_list(metrics, key, value, overwrite)
    elif single_value:
        return handle_metric_single(metrics, key, value, overwrite)
    return handle_metric_list_append(metrics, key, value, overwrite)


def handle_metric_single(
    metrics: dict[str, MetricType],
    key: str,
    value: float | int,
    overwrite: bool,
) -> dict:
    """
    Handle metric single value.

    Parameters
    ----------
    metrics : dict[str, MetricType]
        Metrics dictionary.
    key : str
        Key of the metric.
    value : float
        Value of the metric.
    overwrite : bool
        If True, overwrite existing metric.

    Returns
    -------
    dict
        Metrics dictionary.
    """
    if key not in metrics or overwrite:
        metrics[key] = value
    return metrics


def handle_metric_list_append(
    metrics: dict[str, MetricType],
    key: str,
    value: float | int,
    overwrite: bool,
) -> dict:
    """
    Handle metric list append.

    Parameters
    ----------
    metrics : dict[str, MetricType]
        Metrics dictionary.
    key : str
        Key of the metric.
    value : float
        Value of the metric.
    overwrite : bool
        If True, overwrite existing metric.

    Returns
    -------
    dict
        Metrics dictionary.
    """
    if key not in metrics or overwrite:
        metrics[key] = [value]
    elif isinstance(metrics[key], list):
        metrics[key].append(value)
    else:
        metrics[key] = [metrics[key], value]
    return metrics


def handle_metric_list(
    metrics: dict[str, MetricType],
    key: str,
    value: list[int | float],
    overwrite: bool,
) -> dict:
    """
    Handle metric list.

    Parameters
    ----------
    metrics : dict[str, MetricType]
        Metrics dictionary.
    key : str
        Key of the metric.
    value : list[int | float]
        Value of the metric.
    overwrite : bool
        If True, overwrite existing metric.

    Returns
    -------
    dict
        Metrics dictionary.
    """
    if key not in metrics or overwrite:
        metrics[key] = value
    else:
        metrics[key].extend(value)
    return metrics
