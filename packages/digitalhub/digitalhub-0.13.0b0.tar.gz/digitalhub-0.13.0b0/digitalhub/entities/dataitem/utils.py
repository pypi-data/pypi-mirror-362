# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import shutil
import typing
from typing import Any

from digitalhub.context.api import get_context
from digitalhub.entities._base.entity._constructors.uuid import build_uuid
from digitalhub.entities._base.material.utils import build_log_path_from_source, eval_local_source
from digitalhub.entities._commons.enums import EntityKinds, EntityTypes
from digitalhub.stores.data.api import get_store
from digitalhub.stores.readers.data.api import get_reader_by_object
from digitalhub.utils.enums import FileExtensions
from digitalhub.utils.generic_utils import slugify_string
from digitalhub.utils.types import SourcesOrListOfSources

if typing.TYPE_CHECKING:
    from digitalhub.entities.dataitem._base.entity import Dataitem


DEFAULT_EXTENSION = FileExtensions.PARQUET.value


def eval_source(
    source: SourcesOrListOfSources | None = None,
    data: Any | None = None,
    kind: str | None = None,
    name: str | None = None,
    project: str | None = None,
) -> Any:
    """
    Evaluate if source is local.

    Parameters
    ----------
    source : SourcesOrListOfSources
        Source(s).

    Returns
    -------
    None
    """
    if (source is None) == (data is None):
        raise ValueError("You must provide source or data.")

    if source is not None:
        eval_local_source(source)
        return source

    if kind == EntityKinds.DATAITEM_TABLE.value:
        ctx = get_context(project)
        pth = ctx.root / f"{slugify_string(name)}.{DEFAULT_EXTENSION}"
        reader = get_reader_by_object(data)
        reader.write_parquet(data, pth)
        return str(pth)

    raise NotImplementedError


def eval_data(
    project: str,
    kind: str,
    source: SourcesOrListOfSources,
    data: Any | None = None,
    file_format: str | None = None,
    engine: str | None = None,
) -> Any:
    """
    Evaluate data is loaded.

    Parameters
    ----------
    project : str
        Project name.
    source : str
        Source(s).
    data : Any
        Dataframe to log. Alternative to source.
    file_format : str
        Extension of the file.
    engine : str
        Engine to use.

    Returns
    -------
    None
    """
    if kind == EntityKinds.DATAITEM_TABLE.value:
        if data is None:
            return get_store(project, source).read_df(
                source,
                file_format=file_format,
                engine=engine,
            )
    return data


def process_kwargs(
    project: str,
    name: str,
    kind: str,
    source: SourcesOrListOfSources,
    data: Any | None = None,
    path: str | None = None,
    **kwargs,
) -> dict:
    """
    Process spec kwargs.

    Parameters
    ----------
    project : str
        Project name.
    name : str
        Object name.
    kind : str
        Kind the object.
    source : SourcesOrListOfSources
        Source(s).
    data : Any
        Dataframe to log. Alternative to source.
    path : str
        Destination path of the entity. If not provided, it's generated.
    **kwargs : dict
        Spec parameters.

    Returns
    -------
    dict
        Kwargs updated.
    """
    if data is not None:
        if kind == EntityKinds.DATAITEM_TABLE.value:
            reader = get_reader_by_object(data)
            kwargs["schema"] = reader.get_schema(data)
    if path is None:
        uuid = build_uuid()
        kwargs["uuid"] = uuid
        kwargs["path"] = build_log_path_from_source(project, EntityTypes.DATAITEM.value, name, uuid, source)
    else:
        kwargs["path"] = path
    return kwargs


def clean_tmp_path(pth: SourcesOrListOfSources) -> None:
    """
    Clean temporary path.

    Parameters
    ----------
    pth : SourcesOrListOfSources
        Path to clean.

    Returns
    -------
    None
    """
    if isinstance(pth, list):
        for p in pth:
            shutil.rmtree(p, ignore_errors=True)
        return
    shutil.rmtree(pth, ignore_errors=True)


def post_process(obj: Dataitem, data: Any) -> Dataitem:
    """
    Post process object.

    Parameters
    ----------
    obj : Dataitem
        The object.
    data : Any
        The data.

    Returns
    -------
    Dataitem
        The object.
    """
    if obj.kind == EntityKinds.DATAITEM_TABLE.value:
        reader = get_reader_by_object(data)
        obj.status.preview = reader.get_preview(data)
        obj.save(update=True)
    return obj
