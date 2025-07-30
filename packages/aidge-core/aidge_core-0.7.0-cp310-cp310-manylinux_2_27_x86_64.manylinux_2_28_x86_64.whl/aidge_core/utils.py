"""
Copyright (c) 2023 CEA-List

This program and the accompanying materials are made available under the
terms of the Eclipse Public License 2.0 which is available at
http://www.eclipse.org/legal/epl-2.0.

SPDX-License-Identifier: EPL-2.0
"""

import queue
import requests
import tqdm
import threading
import subprocess
import pathlib
from typing import List
from inspect import signature
from functools import wraps
from typing import Union, _SpecialForm, List, Mapping, Dict, Tuple, get_origin, get_args
from contextlib import contextmanager

from aidge_core import Log

def template_docstring(template_keyword, text_to_replace):
    """Method to template docstring

    :param template: Template keyword to replace, in the documentation you template word must be between `{` `}`
    :type template: str
    :param text_to_replace: Text to replace your template with.
    :type text_to_replace: str
    """

    def dec(func):
        if "{" + template_keyword + "}" not in func.__doc__:
            raise RuntimeError(
                f"The function {func.__name__} docstring does not contain the template keyword: {template_keyword}."
            )
        func.__doc__ = func.__doc__.replace(
            "{" + template_keyword + "}", text_to_replace
        )
        return func

    return dec


def is_instance_of(obj, typ) -> bool:
    """Check if an object is an instance of a type.
    With a special handling for subscripted types.
    """
    origin = get_origin(typ)
    args = get_args(typ)

    # If it's not a generic type, fallback to normal isinstance check
    if origin is None:
        return isinstance(obj, typ)

    # Check if the object is of the expected container type
    if not isinstance(obj, origin):
        return False

    # Handle specific cases for List, Dict, Tuple
    if origin in (list, set):
        return all(is_instance_of(item, args[0]) for item in obj)
    if origin is dict:
        return all(is_instance_of(k, args[0]) and is_instance_of(v, args[1]) for k, v in obj.items())
    if origin is tuple:
        if len(args) == 2 and args[1] is ...:  # Handles Tuple[X, ...]
            return all(is_instance_of(item, args[0]) for item in obj)
        return len(obj) == len(args) and all(is_instance_of(item, t) for item, t in zip(obj, args))

    raise NotImplementedError(f"Type {origin} is not supported")

def type_to_str(typ) -> str:
    """Return a string describing the type given as an argument.
    With a special handling for subscripted types.
    This gives a more detail than the __name__ attribute of the type.

    Example: dict[str, list[list[int]]] instead of dict.
    """
    origin = get_origin(typ)
    args = get_args(typ)

    if origin is None:
        return typ.__name__
    if origin in (list, set):
        return f"{origin.__name__}[{type_to_str(args[0])}]"
    if origin is dict:
        return f"{origin.__name__}[{type_to_str(args[0])}, {type_to_str(args[1])}]"
    if origin is tuple:
        if len(args) == 2 and args[1] is ...:
            return f"{origin.__name__}[{type_to_str(args[0])}, ...]"
        return f"{origin.__name__}[{', '.join(type_to_str(t) for t in args)}]"
    raise NotImplementedError(f"Type {origin} is not supported")

def var_to_type_str(var) -> str:
    """Return a string describing the type of a variable.
    With a special handling for subscripted types.
    """
    typ = type(var)
    if typ is list and var:
        return f"list[{var_to_type_str(var[0])}]"
    if typ is set and var:
        return f"set[{var_to_type_str(next(iter(var)))}]"
    if typ is dict and var:
        key_type = var_to_type_str(next(iter(var.keys())))
        value_type = var_to_type_str(next(iter(var.values())))
        return f"dict[{key_type}, {value_type}]"
    if typ is tuple and var:
        return f"tuple[{', '.join(var_to_type_str(v) for v in var)}]"
    return typ.__name__

def check_types(f):
    """Decorator used to automatically check type of functions/methods.
    To do so, we use type annotation available since Python 3.5 https://docs.python.org/3/library/typing.html.
    Typing check is done with an handling of subscripted types (List, Dict, Tuple).
    """
    sig = signature(f)

    # Dictionary key : param name, value : annotation
    args_types = {p.name: p.annotation \
            for p in sig.parameters.values()}

    @wraps(f)
    def decorated(*args, **kwargs):
        bind = sig.bind(*args, **kwargs)
        obj_name = ""

        # Check if we are in a method !
        if "self" in sig.parameters:
            obj_name = f"{bind.args[0].__class__.__name__}."

        for value, typ in zip(bind.args, args_types.items()):
            annotation_type = typ[1]
            if annotation_type == sig.empty:
                pass
            if type(annotation_type) is _SpecialForm and annotation_type._name == "Any": # check if Any
                continue
            if value is None: # None value is always accepted
                continue
            if hasattr(annotation_type, "__origin__") and annotation_type.__origin__ is Union: # check if Union
                    # Types are contained in the __args__ attribute which is a list
                    # isinstance only support type or tuple, so we convert to tuple
                    annotation_type = tuple(annotation_type.__args__)
            if annotation_type != sig.empty and not is_instance_of(value, annotation_type):
                raise TypeError(f'In {obj_name}{f.__name__}: \"{typ[0]}\" parameter must be of type {type_to_str(annotation_type)} but is of type {var_to_type_str(value)} instead.')
        return f(*args, **kwargs)
    return decorated


def run_command(command: List[str], cwd: pathlib.Path = None):
    """
    This function has the job to run a command and return stdout and stderr that are not shown
    by subprocess.check_call / call.
    If the subprocess returns smthg else than 0, it will raise an error.
    Arg:
        command : written with the same syntax as subprocess.call
        cwd : path from where the command must be called

    Call example:
    ```python

        cmd = run_command(
                        [
                            "cmake",
                            str(self.EXPORT_PATH.absolute()),
                            "-DPYBIND=1",
                            f"-DCMAKE_INSTALL_PREFIX:PATH={install_path}",
                        ],
                        cwd=str(self.BUILD_DIR),
                    )
            try:
            for std_line in cmd:
                print(std_line, end="")
        except subprocess.CalledProcessError as e:
            print(f"An error occurred: {e}\nFailed to configure export.")

        # TO RETRIEVE THE RETURN CODE AFTER EXECUTION
        return_code = next(cmd,0)
    ```
    """

    process = subprocess.Popen(
        command, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )

    stdout_queue = queue.Queue()
    stderr_queue = queue.Queue()

    def enqueue_output(stream, queue_to_append):
        for line in iter(stream.readline, ""):
            queue_to_append.put(line)
        stream.close()

    stdout_thread = threading.Thread(
        target=enqueue_output, args=(process.stdout, stdout_queue)
    )
    stderr_thread = threading.Thread(
        target=enqueue_output, args=(process.stderr, stderr_queue)
    )
    stdout_thread.start()
    stderr_thread.start()

    while (
        stdout_thread.is_alive()
        or stderr_thread.is_alive()
        or not stdout_queue.empty()
        or not stderr_queue.empty()
    ):
        try:
            stdout_line = stdout_queue.get_nowait()
            yield stdout_line
        except queue.Empty:
            pass

        try:
            stderr_line = stderr_queue.get_nowait()
            yield stderr_line
        except queue.Empty:
            pass

    return_code = process.wait()
    Log.debug(f"Done executing command : {' '.join(map(str, command))}\nreturn code: {return_code}")
    if return_code != 0:
        raise subprocess.CalledProcessError(return_code, command)
    return return_code



@contextmanager
def _dummy_tqdm():
    class DummyBar:
        def update(self, _): pass
        def close(self): pass
    yield DummyBar()

def download_file(file_path: Union[str, pathlib.Path], file_url: str, block_size: int = 8192, show_progress: bool = True):
    """Download a file from a given URL to the specified local path.
    If the file already exists at the destination, the download is skipped.

    :param file_path: The destination file path. Can be a string or a pathlib.Path object.
    :type file_path: str or pathlib.Path
    :param file_url: The URL of the file to download.
    :type file_url: str
    :param block_size: The chunk size (in bytes) to use when downloading the file. Defaults to 8192 bytes.
    :type block_size: int, optional
    :param show_progress: Whether to display a progress bar during download. Defaults to True.
    :type show_progress: bool, optional
    """
    if isinstance(file_path, str):
        file_path = pathlib.Path(file_path)
    if file_path.exists():
        Log.info(f"{file_path.name} already exists.")
        return

    Log.info(f"{file_path.name} not found. Downloading...")

    try:
        response = requests.get(file_url, stream=True)
        response.raise_for_status()

        # Get the total file size from headers
        total_size = int(response.headers.get("content-length", 0))
        progress_context = (
            tqdm.tqdm(
                total=total_size,
                unit='B',
                unit_scale=True,
                unit_divisor=1024,
                desc=file_path.name
            ) if show_progress else
            _dummy_tqdm()
        )

        # Create a progress bar
        with progress_context as progress_bar:
            with open(file_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=block_size):
                    if chunk:
                        f.write(chunk)
                        progress_bar.update(len(chunk))

        Log.notice(f"\nDownloaded {file_path.name} successfully.")

    except requests.exceptions.RequestException as e:
        Log.error(f"Failed to download the file: {e}")
