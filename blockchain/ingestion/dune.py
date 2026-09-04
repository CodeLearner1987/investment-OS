"""Dune API adapter for saved SQL queries and indexed blockchain analytics."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any
from urllib.request import Request, urlopen


@dataclass(frozen=True)
class DuneClient:
    api_key: str
    base_url: str = "https://api.dune.com/api/v1"
    timeout: float = 60.0

    @classmethod
    def from_env(cls) -> "DuneClient":
        key = os.getenv("DUNE_API_KEY")
        if not key:
            raise ValueError("Missing DUNE_API_KEY")
        return cls(api_key=key)

    def _request(self, method: str, path: str, body: dict[str, Any] | None = None) -> dict[str, Any]:
        data = None if body is None else json.dumps(body).encode("utf-8")
        request = Request(
            self.base_url + path,
            data=data,
            headers={"X-Dune-API-Key": self.api_key, "Content-Type": "application/json"},
            method=method,
        )
        with urlopen(request, timeout=self.timeout) as response:
            return json.loads(response.read().decode("utf-8"))

    def execute_query(self, query_id: int, parameters: list[dict[str, Any]] | None = None) -> dict[str, Any]:
        body = {"query_id": query_id}
        if parameters:
            body["query_parameters"] = parameters
        return self._request("POST", "/query/execute", body)

    def execution_results(self, execution_id: str) -> dict[str, Any]:
        return self._request("GET", f"/query/{execution_id}/results")
