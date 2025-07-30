from .client import Client
from collections.abc import Generator

__all__ = ['create_default_repl_scope']

def create_default_repl_scope(client: Client) -> Generator[dict[str, object], None, None]: ...
