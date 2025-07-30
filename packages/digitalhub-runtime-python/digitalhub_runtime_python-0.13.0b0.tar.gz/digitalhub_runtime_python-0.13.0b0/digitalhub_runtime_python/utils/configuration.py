# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from pathlib import Path
from typing import Callable, Union

from digitalhub.stores.data.s3.utils import get_bucket_and_key, get_s3_source
from digitalhub.utils.generic_utils import (
    decode_base64_string,
    extract_archive,
    import_function,
    requests_chunk_download,
)
from digitalhub.utils.git_utils import clone_repository
from digitalhub.utils.logger import LOGGER
from digitalhub.utils.uri_utils import (
    get_filename_from_uri,
    has_git_scheme,
    has_local_scheme,
    has_remote_scheme,
    has_s3_scheme,
    has_zip_scheme,
)


def import_function_from_source(path: Path, source_spec: dict) -> Callable:
    """
    Get function from source.

    Parameters
    ----------
    path : Path
        Path where to save the function source.
    source_spec : dict
        Funcrion source spec.

    Returns
    -------
    Callable
        Function.
    """
    try:
        source_path = save_function_source(path, source_spec)
        handler_path, function_name = parse_handler(source_spec["handler"])
        function_path = (source_path / handler_path).with_suffix(".py")
        return import_function(function_path, function_name)
    except Exception as e:
        msg = f"Some error occurred while getting function. Exception: {e.__class__}. Error: {e.args}"
        LOGGER.exception(msg)
        raise RuntimeError(msg) from e


def save_function_source(path: Path, source_spec: dict) -> Path:
    """
    Save function source.

    Parameters
    ----------
    path : Path
        Path where to save the function source.
    source_spec : dict
        Function source spec.

    Returns
    -------
    Path
        Path to the function source.
    """
    # Prepare path
    path.mkdir(parents=True, exist_ok=True)

    # Get relevant information
    base64 = source_spec.get("base64")
    source = source_spec.get("source")

    # Base64
    if base64 is not None:
        base64_path = path / "main.py"
        base64_path.write_text(decode_base64_string(base64))
        return base64_path

    if source is None:
        raise RuntimeError("Function source not found in spec.")

    # Git repo
    if has_git_scheme(source):
        clone_repository(path, source)

    # Http(s) or s3 presigned urls
    elif has_remote_scheme(source):
        filename = path / get_filename_from_uri(source)
        if has_zip_scheme(source):
            requests_chunk_download(source.removeprefix("zip+"), filename)
            extract_archive(path, filename)
            filename.unlink()
        else:
            requests_chunk_download(source, filename)

    # S3 path
    elif has_s3_scheme(source):
        if not has_zip_scheme(source):
            raise RuntimeError("S3 source must be a zip file with scheme zip+s3://.")
        filename = path / get_filename_from_uri(source)
        bucket, key = get_bucket_and_key(source)
        get_s3_source(bucket, key, filename)
        extract_archive(path, filename)
        filename.unlink()

    # Unsupported scheme
    else:
        raise RuntimeError("Unable to collect source.")

    return path


def import_function_and_init_from_source(
    path: Path,
    source_spec: dict,
    default_py: str,
) -> tuple[Callable, Union[Callable, None]]:
    """
    Import function and init from source.

    Parameters
    ----------
    path : Path
        Path where the function source is or must be saved.
    source_spec : dict
        Function source.
    default_py : str
        Default python file.

    Returns
    -------
    tuple
        Function and init function.
    """

    # Get function source
    function_path = get_function_source(path, source_spec, default_py)
    _, handler_name = parse_handler(source_spec.get("handler"))

    # Import function
    fnc = import_function(function_path, handler_name)

    # Get init function
    init_fnc: Callable | None = None
    init_handler: str | None = source_spec.get("init_function")
    if init_handler is not None:
        init_fnc = import_function(function_path, init_handler)

    return fnc, init_fnc


def get_function_source(path: Path, source_spec: dict, default_py: str) -> Path:
    """
    Get function source.

    Parameters
    ----------
    path : Path
        Path where the function source is or must be saved.
    source_spec : dict
        Function source.
    default_py : str
        Default python file.

    Returns
    -------
    Path
        Path to function source.
    """
    # Get relevant information
    base64 = source_spec.get("base64")
    source = source_spec.get("source", default_py)
    handler = source_spec.get("handler")

    handler_path, _ = parse_handler(handler)

    # Check base64. If it is set, it means
    # that the source comes from a local file
    if base64 is not None:
        if has_local_scheme(source):
            return path / handler_path / Path(source)
        raise RuntimeError("Source is not a local file.")

    if handler_path != Path(""):
        return path / handler_path.with_suffix(".py")
    raise RuntimeError("Must provide handler path in handler in form <root>.<dir>.<module>:<function_name>.")


def parse_handler(handler: str) -> tuple[Path, str]:
    """
    Parse handler.

    Parameters
    ----------
    handler : str
        Function handler.

    Returns
    -------
    tuple[Path, str]
        Handler path and function name.
    """
    parsed = handler.split(":")
    if len(parsed) == 1:
        return Path(""), parsed[0]
    return Path(*parsed[0].split(".")), parsed[1]
