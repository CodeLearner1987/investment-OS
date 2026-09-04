"""Etherscan API v2 adapter for indexed Ethereum evidence."""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any
from urllib.parse import urlencode
from urllib.request import urlopen
import json


class EtherscanError(RuntimeError):
    """Raised when Etherscan returns an API error."""


@dataclass(frozen=True)
class EtherscanClient:
    api_key: str
    base_url: str = "https://api.etherscan.io/v2/api"
    chain_id: int = 1
    timeout: float = 30.0

    @classmethod
    def from_env(cls) -> "EtherscanClient":
        key = os.getenv("ETHERSCAN_API_KEY")
        if not key:
            raise ValueError("Missing ETHERSCAN_API_KEY")
        return cls(api_key=key)

    def request(self, action: str, **params: Any) -> list[dict[str, Any]] | dict[str, Any]:
        query = {
            "chainid": self.chain_id,
            "module": "account",
            "action": action,
            "apikey": self.api_key,
            **params,
        }
        with urlopen(f"{self.base_url}?{urlencode(query)}", timeout=self.timeout) as response:
            payload = json.loads(response.read().decode("utf-8"))
        if str(payload.get("status")) == "0" and payload.get("message") not in {"No transactions found", "No records found"}:
            raise EtherscanError(str(payload.get("result", payload)))
        result = payload.get("result", [])
        return result

    def erc20_transfers(self, address: str, startblock: int = 0, endblock: int = 99999999,
                        contractaddress: str | None = None) -> list[dict[str, Any]]:
        return self.request(
            "tokentx",
            address=address,
            startblock=startblock,
            endblock=endblock,
            sort="asc",
            **({"contractaddress": contractaddress} if contractaddress else {}),
        )
