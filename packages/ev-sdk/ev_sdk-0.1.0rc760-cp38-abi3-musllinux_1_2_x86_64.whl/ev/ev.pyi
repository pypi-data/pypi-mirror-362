from __future__ import annotations

from typing import Callable

def main(): ...

class _Client:
    #
    @staticmethod
    def default() -> _Client: ...
    #
    def run(self, job: _Job, args: dict[str, str]) -> _JobHandle: ...

class _Function:
    #
    @staticmethod
    def from_code(py_name: str, py_code: str): ...
    #
    @staticmethod
    def from_callable(py_name: str, py_callable: Callable): ...

class _Job:
    #
    name: str
    main: _Function | None
    #
    @staticmethod
    def new(name: str, env: _Env) -> _Job: ...

class _JobHandle:
    job_id: str
    job_url: str
    space_id: str

class _Env:
    #
    @staticmethod
    def new(python_version: str) -> _Env: ...
    #
    @property
    def environ(self) -> dict[str, str]: ...
    #
    @environ.setter
    def environ(self, env: dict[str, str]): ...
    #
    def include(self, paths: list[str]): ...
    #
    def pip_install(self, requirements: list[str]): ...
    #
    def dump(self) -> dict[str, str]: ...
