"""Minimal JSON-RPC client for primary blockchain evidence.

No third-party dependency is required. Credentials/endpoints are read from
arguments or environment variables; secrets are never stored in the repo.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any
from urllib.request import Request, urlopen


class RPCError(RuntimeError):
    """Raised when an Ethereum JSON-RPC request fails."""


@dataclass(frozen=True)
class EthereumRPC:
    url: str
    timeout: float = 30.0

    @classmethod
    def from_env(cls, variable: str = "ETHEREUM_RPC_URL") -> "EthereumRPC":
        url = os.getenv(variable)
        if not url:
            raise ValueError(f"Missing {variable}; set an Ethereum RPC endpoint")
        return cls(url=url)

    def call(self, method: str, params: list[Any] | None = None) -> Any:
        payload = json.dumps({
            "jsonrpc": "2.0",
            "id": 1,
            "method": method,
            "params": params or [],
        }).encode("utf-8")
        request = Request(
            self.url,
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urlopen(request, timeout=self.timeout) as response:
            body = json.loads(response.read().decode("utf-8"))
        if "error" in body:
            raise RPCError(str(body["error"]))
        return body.get("result")

    def get_logs(self, from_block: int | str, to_block: int | str, address: str | None = None,
                 topics: list[str | None] | None = None) -> list[dict[str, Any]]:
        params: dict[str, Any] = {
            "fromBlock": hex(from_block) if isinstance(from_block, int) else from_block,
            "toBlock": hex(to_block) if isinstance(to_block, int) else to_block,
        }
        if address:
            params["address"] = address
        if topics:
            params["topics"] = topics
        return self.call("eth_getLogs", [params])

    def get_transaction_receipt(self, tx_hash: str) -> dict[str, Any] | None:
        return self.call("eth_getTransactionReceipt", [tx_hash])

    def get_block(self, block_number: int | str) -> dict[str, Any] | None:
        tag = hex(block_number) if isinstance(block_number, int) else block_number
        return self.call("eth_getBlockByNumber", [tag, False])
