"""Deterministic DEX economic-event reconstruction primitives.

This module does not guess from token transfers alone. A caller must provide
both sides of an observed swap, including the trader and venue. Unknown or
ambiguous routing stays unresolved rather than being promoted to a buy/sell.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

from blockchain.schema.evidence import Evidence, EvidenceLevel, EventType


@dataclass(frozen=True)
class SwapLeg:
    asset: str
    amount: Decimal


@dataclass(frozen=True)
class DexSwap:
    tx_hash: str
    chain: str
    block_number: int
    timestamp: object
    trader: str
    venue: str
    sold: SwapLeg
    bought: SwapLeg
    contract: str | None = None
    source: str = "decoded_swap"


def reconstruct_swap(swap: DexSwap, target_asset: str) -> Evidence:
    """Turn a fully observed swap into VERIFIED_BUY/VERIFIED_SELL evidence."""
    sold = swap.sold
    bought = swap.bought

    if sold.amount <= 0 or bought.amount <= 0:
        raise ValueError("Swap amounts must be positive")

    if bought.asset == target_asset and sold.asset != target_asset:
        event_type = EventType.VERIFIED_BUY
        amount = bought.amount
        counter_asset = sold.asset
        counter_amount = sold.amount
    elif sold.asset == target_asset and bought.asset != target_asset:
        event_type = EventType.VERIFIED_SELL
        amount = sold.amount
        counter_asset = bought.asset
        counter_amount = bought.amount
    else:
        raise ValueError("Swap does not represent a one-sided target asset exchange")

    return Evidence(
        chain=swap.chain,
        tx_hash=swap.tx_hash,
        block_number=swap.block_number,
        timestamp=swap.timestamp,
        event_type=event_type,
        level=EvidenceLevel.FACT,
        asset=target_asset,
        sender=swap.trader,
        receiver=swap.trader,
        amount=amount,
        counter_asset=counter_asset,
        counter_amount=counter_amount,
        venue=swap.venue,
        contract=swap.contract,
        source=swap.source,
        metadata={"reconstruction": "two_sided_swap"},
    )
