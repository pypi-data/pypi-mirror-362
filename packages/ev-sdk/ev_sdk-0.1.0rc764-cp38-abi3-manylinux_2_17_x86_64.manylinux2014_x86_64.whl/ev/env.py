from __future__ import annotations

import functools
import inspect
import os
import platform
from collections.abc import MutableMapping

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
            calling_dir = os.path.dirname(os.path.abspath(calling_file))
        else:
            calling_dir = os.getcwd()

        self._env.include([os.path.join(calling_dir, paths)])
        return self

    @include.register(list)
    def _(self, paths: list[str]) -> Env:
        # The file that the "include" is called from is two frames above the current frame
        # because of the functools.singledispatchmethod decorator.
        frame = inspect.currentframe()
        if frame and frame.f_back and frame.f_back.f_back:
            calling_file = frame.f_back.f_back.f_code.co_filename
            calling_dir = os.path.dirname(os.path.abspath(calling_file))
        else:
            calling_dir = os.getcwd()

        paths = [os.path.join(calling_dir, path) for path in paths]
        self._env.include(paths)
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
            calling_dir = os.path.dirname(os.path.abspath(calling_file))
        else:
            calling_dir = os.getcwd()
        requirements_path = os.path.join(calling_dir, requirements)

        # consider a library, but this will suffice.
        lines = []
        with open(requirements_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    lines.append(line)

        # adds all the parsed requirements
        self._env.pip_install(lines)
        return self

    @pip_install.register(list)
    def _(self, requirements: list[str]) -> Env:
        self._env.pip_install(requirements)
        return self
