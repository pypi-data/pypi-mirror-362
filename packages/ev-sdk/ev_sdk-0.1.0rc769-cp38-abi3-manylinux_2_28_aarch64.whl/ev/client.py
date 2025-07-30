from __future__ import annotations

from .ev import _Client


class Client:
    """The main client for interacting with the Eventual (ev) platform.

    This client provides access to all ev platform services including compute clusters,
    job management, deployments, and other platform resources. The client handles
    authentication, connection management, and provides a high-level interface for
    platform operations.

    Note:
        Direct instantiation using `Client()` is not supported. Use the `default()`
        class method to create client instances.

    Example:
        Create a client instance using the default configuration:

        >>> client = Client.default()
        >>> print(client)

    See Also:
        Client.default(): Factory method for creating client instances with default settings.
    """

    _client: _Client

    def __init__(self):
        """Initialize Client instance.

        Raises:
            ValueError: Always raised as direct instantiation is not supported.
                       Use Client.default() instead.
        """
        raise ValueError("Client.__init__ is not supported.")

    @staticmethod
    def default() -> Client:
        """Creates a default ev client instance."""
        client = Client.__new__(Client)
        client._client = _Client.default()
        return client

    def __repr__(self) -> str:
        """Return string representation of the client.

        Returns:
            str: String representation of the underlying client.
        """
        return self._client.__repr__()
