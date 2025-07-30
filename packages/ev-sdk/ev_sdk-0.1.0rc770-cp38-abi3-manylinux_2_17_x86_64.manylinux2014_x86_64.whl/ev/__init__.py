"""Eventual Python SDK.

This package provides the Python client library for interacting with the Eventual platform.
It includes tools for creating and managing jobs, environments, and platform resources.

Main Components:
    Client: The main client for platform interactions
    Job: Represents programs that can be run on the Eventual platform
    JobHandle: Information about running jobs
    Env: Environment configuration for jobs

Example:
    >>> from ev import Client, Job
    >>> client = Client.default()
    >>> job = Job("my-job")
"""

from .client import Client
from .env import Env
from .job import Job, JobHandle

__all__ = [
    "Client",
    "Env",
    "Job",
    "JobHandle",
]
