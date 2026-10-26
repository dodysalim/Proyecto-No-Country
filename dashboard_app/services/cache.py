"""Caché con caducidad sobre un diccionario de sesión (p. ej. `st.session_state`)."""
import time
from typing import Any, Callable, MutableMapping, Optional


class TimedCache:
    def __init__(self, store: MutableMapping, key: str, ttl_seconds: float, clock: Callable[[], float] = time.time):
        self._store, self._key, self._ttl, self._clock = store, key, ttl_seconds, clock
        if key not in store:
            store[key] = None
            store[f"{key}__ts"] = None

    @property
    def value(self) -> Any:
        return self._store[self._key]

    @property
    def is_fresh(self) -> bool:
        ts = self._store[f"{self._key}__ts"]
        return self.value is not None and ts is not None and (self._clock() - ts) <= self._ttl

    def set(self, value: Any) -> None:
        self._store[self._key] = value
        self._store[f"{self._key}__ts"] = self._clock()

    def clear(self) -> None:
        self._store[self._key] = None
        self._store[f"{self._key}__ts"] = None

    def get_or_load(self, loader: Callable[[], Any]) -> Any:
        if not self.is_fresh:
            self.set(loader())
        return self.value
