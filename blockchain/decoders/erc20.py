"""Dependency-free ERC-20 Transfer log decoder."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

# keccak256("Transfer(address,address,uint256)")
TRANSFER_TOPIC = "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a9df523b3ef"


@dataclass(frozen=True)
class ERC20Transfer:
    contract: str
    sender: str
    receiver: str
    raw_amount: int
    amount: Decimal
    decimals: int
    tx_hash: str
    block_number: int
    log_index: int


def _address(topic: str) -> str:
    return "0x" + topic[-40:]


def decode_transfer(log: dict, decimals: int = 18) -> ERC20Transfer | None:
    topics = log.get("topics", [])
    if len(topics) < 3 or topics[0].lower() != TRANSFER_TOPIC:
        return None
    raw = int(log.get("data", "0x0"), 16)
    return ERC20Transfer(
        contract=log["address"],
        sender=_address(topics[1]),
        receiver=_address(topics[2]),
        raw_amount=raw,
        amount=Decimal(raw) / (Decimal(10) ** decimals),
        decimals=decimals,
        tx_hash=log["transactionHash"],
        block_number=int(log["blockNumber"], 16),
        log_index=int(log["logIndex"], 16),
    )
