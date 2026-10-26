"""Fuente de datos del dashboard.

`JobMarketRepository` define lo que la interfaz necesita; `SupabaseJobRepository`
es una implementación concreta. Las vistas dependen del protocolo, no de Supabase,
así que otra fuente (CSV, PostgreSQL, datos de prueba) se conecta sin cambiar la UI.
"""
from typing import Any, Dict, List, Protocol


class JobMarketRepository(Protocol):
    def fetch_jobs(self) -> List[Dict[str, Any]]: ...
    def fetch_trends(self) -> List[Dict[str, Any]]: ...
    def clear_all(self) -> bool: ...


class SupabaseJobRepository:
    """Adaptador sobre `database.supabase_client.SupabaseClient`."""

    def __init__(self, client=None):
        if client is None:
            from database.supabase_client import SupabaseClient
            client = SupabaseClient()
        self._client = client

    @staticmethod
    def _rows(response) -> List[Dict[str, Any]]:
        return response.data if response and response.data else []

    def fetch_jobs(self) -> List[Dict[str, Any]]:
        return self._rows(self._client.get_jobs(limit=None))

    def fetch_trends(self) -> List[Dict[str, Any]]:
        return self._rows(self._client.get_trends(limit=None))

    def clear_all(self) -> bool:
        return bool(self._client.clear_jobs_table())
