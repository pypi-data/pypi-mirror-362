from __future__ import annotations

import ast
import inspect
import textwrap
from functools import wraps
from types import FunctionType
from typing import Callable

from .client import Client
from .env import Env
from .ev import _Client, _Function, _Job, _JobHandle


class Job:
    """Job represents an ev program that can be run on the Eventual Platform."""

    _job: _Job

    def __init__(self, name: str = "job", env: Env = Env()):
        self._job = _Job.new(name, env._env)

    @property
    def name(self) -> str:
        return self._job.name

    def main(self) -> Callable:
        """This decorator sets the entrypoint for a job."""
        # Capture the job.main() arguments.
        # ... no arguments yet.

        # Creates a regular no-arg decorator.
        def decorator(main: FunctionType) -> Callable:
            # This decorator actually sets the function upon *invocation* i.e. job.main() WITH parens.
            if self._job.main:
                raise ValueError("This job's main has already been set!")

            # Build the internal representation of a function.
            self._job.main = _new_function(main)

            # The decorated function should not be directly callable!
            @wraps(main)
            def no_call():
                raise RuntimeError("The job's main is not directly callable.")

            return no_call

        return decorator

    def run(self, client: Client | None = None, args: dict[str, str] = {}) -> JobHandle:
        """Runs the job to the eventual platform, returning a job handle."""
        _client: _Client = client._client if client else Client.default()._client
        _handle = _client.run(self._job, args)
        return JobHandle(_handle)


def _new_function(func: FunctionType) -> _Function:
    """Builds the internal representation of a function.

    Note:
        The function must be defined at a module top-level for now!
    """
    module = inspect.getmodule(func)

    # We need the file so we can include it for packaging (TODO).
    if not hasattr(module, "__file__"):
        raise ValueError("An ev function must be declared in a file-based module.")

    # Assert the function is NOT defined in a local scope.
    if "<locals>" in func.__qualname__.split("."):
        raise ValueError("An ev function must be declared at a module's top level.")

    # We only need the function's name and its source code, then we can generate the modules.
    py_name = func.__qualname__
    py_code = _get_function_code(func)

    return _Function.from_code(
        py_name,
        py_code,
    )


def _get_function_code(func: FunctionType) -> str:
    """Get's the undecorated source of a function definition."""
    src = inspect.getsource(func)
    src = textwrap.dedent(src)
    tree = ast.parse(src)
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == func.__name__:
            node.decorator_list = [] # strip the decorator
            return ast.unparse(node)
    raise ValueError(f"Function {func.__name__} was not found in the AST.")


class JobHandle:
    """JobHandle holds information about a running job."""
    _handle: _JobHandle

    def __init__(self, _handle: _JobHandle):
        self._handle = _handle

    @property
    def job_id(self) -> str:
        """Returns the job id."""
        return self._handle.job_id

    @property
    def job_url(self) -> str:
        """Returns the job url on the Eventual Platform dashboard."""
        return self._handle.job_url

    @property
    def space_id(self) -> str:
        """Returns the space where this job was submitted to."""
        return self._handle.space_id
