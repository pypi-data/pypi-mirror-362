# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import base64
import importlib.util as imputil
import json
from datetime import date, datetime, time
from enum import Enum, EnumMeta
from pathlib import Path
from types import MappingProxyType
from typing import Any, Callable
from warnings import warn
from zipfile import ZipFile

import numpy as np
import requests
from slugify import slugify

from digitalhub.utils.io_utils import read_text


def get_timestamp() -> str:
    """
    Get the current timestamp timezoned.

    Returns
    -------
    str
        The current timestamp.
    """
    return datetime.now().astimezone().isoformat()


def decode_base64_string(string: str) -> str:
    """
    Decode a string from base64.

    Parameters
    ----------
    string : str
        The string to decode.

    Returns
    -------
    str
        The string decoded from base64.
    """
    return base64.b64decode(string).decode()


def encode_string(string: str) -> str:
    """
    Encode a string in base64.

    Parameters
    ----------
    string : str
        The string to encode.

    Returns
    -------
    str
        The string encoded in base64.
    """
    return base64.b64encode(string.encode()).decode()


def encode_source(path: str) -> str:
    """
    Read a file and encode in base64 the content.

    Parameters
    ----------
    path : str
        The file path to read.

    Returns
    -------
    str
        The file content encoded in base64.
    """
    return encode_string(read_text(path))


def requests_chunk_download(source: str, filename: Path) -> None:
    """
    Download a file in chunks.

    Parameters
    ----------
    source : str
        URL to download the file.
    filename : Path
        Path where to save the file.

    Returns
    -------
    None
    """
    with requests.get(source, stream=True) as r:
        r.raise_for_status()
        with filename.open("wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)


def extract_archive(path: Path, filename: Path) -> None:
    """
    Extract a zip archive.

    Parameters
    ----------
    path : Path
        Path where to extract the archive.
    filename : Path
        Path to the archive.

    Returns
    -------
    None
    """
    with ZipFile(filename, "r") as zip_file:
        zip_file.extractall(path)


class CustomJsonEncoder(json.JSONEncoder):
    """
    Custom JSON encoder to handle json dumps.
    """

    def default(self, obj: Any) -> Any:
        """
        Convert an object to json.

        Parameters
        ----------
        obj : Any
            The object to convert.

        Returns
        -------
        Any
            The object converted to json.
        """
        if isinstance(obj, (int, str, float, list, dict)):
            return obj
        elif isinstance(obj, (np.integer, np.int64)):
            return int(obj)
        elif isinstance(obj, (np.floating, np.float64)):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, (datetime, date, time)):
            return obj.isoformat()
        return str(obj)


def dump_json(struct: Any) -> str:
    """
    Convert a dict to json.

    Parameters
    ----------
    struct : dict
        The dict to convert.

    Returns
    -------
    str
        The json string.
    """
    return json.dumps(struct, cls=CustomJsonEncoder)


def slugify_string(filename: str) -> str:
    """
    Sanitize a filename.

    Parameters
    ----------
    filename : str
        The filename to sanitize.

    Returns
    -------
    str
        The sanitized filename.
    """
    return slugify(filename, max_length=255)


def import_function(path: Path, handler: str) -> Callable:
    """
    Import a function from a module.

    Parameters
    ----------
    path : Path
        Path where the function source is located.
    handler : str
        Function name.

    Returns
    -------
    Callable
        Function.
    """
    spec = imputil.spec_from_file_location(path.stem, path)
    if spec is None:
        raise RuntimeError(f"Error loading function source from {str(path)}.")

    mod = imputil.module_from_spec(spec)
    if spec.loader is None:
        raise RuntimeError(f"Error getting module loader from {str(path)}.")

    spec.loader.exec_module(mod)
    func = getattr(mod, handler)
    if not callable(func):
        raise RuntimeError(f"Handler '{handler}' is not a callable.")

    return func


def list_enum(enum: EnumMeta) -> list[Any]:
    """
    Get all values of an enum.

    Parameters
    ----------
    enum : EnumMeta
        Enum class to get values from.

    Returns
    -------
    list[Any]
        List of enum values.
    """
    vals: MappingProxyType[str, Enum] = enum.__members__
    return [member.value for member in vals.values()]


def carriage_return_warn(string: str) -> None:
    """
    Print a warning message if string contains a carriage return (\r\n).

    Parameters
    ----------
    string : str
        The string to check.

    Returns
    -------
    None
    """
    if "\r\n" in string:
        warn("String contains a carriage return. It may not be parsed correctly from remote runtimes.")


def read_source(path: str) -> str:
    """
    Read a file.

    Parameters
    ----------
    path : Path
        Path to the file.

    Returns
    -------
    str
        File content.
    """
    text = read_text(path)
    carriage_return_warn(text)
    return encode_string(text)
