from __future__ import annotations

from .ev import _Client


class Client:
    _client: _Client

    def __init__(self):
        raise ValueError("Client.__init__ is not supported.")

    @staticmethod
    def default() -> Client:
        """Creates a default ev client instance."""
        client = Client.__new__(Client)
        client._client = _Client.default()
        return client

    def __repr__(self) -> str:
        return self._client.__repr__()
