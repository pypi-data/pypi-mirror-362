from __future__ import annotations

import functools
import inspect
import platform
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import MutableMapping

import pathlib

from .ev import _Env


class Env:
    """Env represents a runtime environment e.g. local files and python dependencies.

    Examples:
        >>> from ev import Env
        >>>
        >>> env = Env("3.11")
        >>> env.pip_install("requirements.txt")
        >>> env.include("/path/to/local.py")
        >>>
        >>> env.environ["foo"] = "bar"
    """

    _env: _Env

    def __init__(self, python_version: str | None = None):
        """Creates an empty environment with the given python version."""
        self._env = _Env.new(python_version or platform.python_version())

    @property
    def environ(self) -> MutableMapping[str, str]:
        """Returns the environment variable object for this environment."""
        return self._env.environ

    @environ.setter
    def environ(self, environ: dict[str, str]):
        """Sets the environment variable object for this environment."""
        self._env.environ = environ

    def _inner_include(self, paths: list[str | Path]) -> None:
        # TODO(sammy): We should pass Path directly to rust instead of passing strings
        self._env.include([path if isinstance(path, str) else path.as_posix() for path in paths])

    @functools.singledispatchmethod
    def include(self, paths: str | list[str]) -> Env:
        """Adds the given file path to this environment, returning itself for chaining.

        Args:
            paths: The file path to include.
        """
        raise TypeError(f"Unsupported argument type, {type(paths)}")

    @include.register(str)
    def _(self, paths: str) -> Env:
        # The file that the "include" is called from is two frames above the current frame
        # because of the functools.singledispatchmethod decorator.
        frame = inspect.currentframe()
        if frame and frame.f_back and frame.f_back.f_back:
            calling_file = frame.f_back.f_back.f_code.co_filename
            calling_dir = pathlib.Path(pathlib.Path(calling_file).resolve()).parent
        else:
            calling_dir = Path.cwd()

        self._inner_include([calling_dir / paths])
        return self

    @include.register(list)
    def _(self, paths: list[str]) -> Env:
        # The file that the "include" is called from is two frames above the current frame
        # because of the functools.singledispatchmethod decorator.
        frame = inspect.currentframe()
        if frame and frame.f_back and frame.f_back.f_back:
            calling_file = frame.f_back.f_back.f_code.co_filename
            calling_dir = pathlib.Path(pathlib.Path(calling_file).resolve()).parent
        else:
            calling_dir = Path.cwd()

        paths = [(calling_dir / path) for path in paths]
        self._inner_include(paths)
        return self

    @functools.singledispatchmethod
    def pip_install(self, requirements: str | list[str]) -> Env:
        """Adds the requirements to this environment, returning itself for chaining.

        See: https://pip.pypa.io/en/stable/reference/requirements-file-format/

        Args:
            requirements: The requirements.txt path (str) or a requirements list.
        """
        raise TypeError("Expected either a requirements file path or list of requirements.")

    @pip_install.register(str)
    def _(self, requirements: str) -> Env:
        # get the directory of the calling file to resolve relative paths
        frame = inspect.currentframe()
        if frame and frame.f_back and frame.f_back.f_back:
            calling_file = frame.f_back.f_back.f_code.co_filename
            calling_dir = pathlib.Path(pathlib.Path(calling_file).resolve()).parent
        else:
            calling_dir = Path.cwd()
        requirements_path = calling_dir / requirements
        # consider a library, but this will suffice.
        lines = []
        with requirements_path.open() as f:
            for line in f:
                stripped_line = line.strip()
                if stripped_line and not stripped_line.startswith("#"):
                    lines.append(stripped_line)

        # adds all the parsed requirements
        self._env.pip_install(lines)
        return self

    @pip_install.register(list)
    def _(self, requirements: list[str]) -> Env:
        self._env.pip_install(requirements)
        return self
