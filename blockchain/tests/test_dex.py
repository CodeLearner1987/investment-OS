"""Tests for economic-event reconstruction."""

from datetime import datetime, timezone
from decimal import Decimal

import pytest

from blockchain.decoders.dex import DexSwap, SwapLeg, reconstruct_swap
from blockchain.schema.evidence import EventType


TS = datetime(2026, 1, 1, tzinfo=timezone.utc)


def swap(sold: str, sold_amount: str, bought: str, bought_amount: str) -> DexSwap:
    return DexSwap(
        tx_hash="0xabc",
        chain="ethereum",
        block_number=1,
        timestamp=TS,
        trader="0xtrader",
        venue="uniswap",
        sold=SwapLeg(sold, Decimal(sold_amount)),
        bought=SwapLeg(bought, Decimal(bought_amount)),
    )


def test_target_acquisition_is_verified_buy():
    evidence = reconstruct_swap(swap("USDC", "100", "TOKEN", "50"), "TOKEN")
    assert evidence.event_type is EventType.VERIFIED_BUY
    assert evidence.amount == Decimal("50")
    assert evidence.counter_amount == Decimal("100")


def test_target_disposal_is_verified_sell():
    evidence = reconstruct_swap(swap("TOKEN", "50", "USDC", "100"), "TOKEN")
    assert evidence.event_type is EventType.VERIFIED_SELL
    assert evidence.amount == Decimal("50")
    assert evidence.counter_amount == Decimal("100")


def test_transfer_is_not_promoted_to_buy_without_two_sided_swap():
    with pytest.raises(ValueError):
        reconstruct_swap(swap("TOKEN", "50", "TOKEN", "50"), "TOKEN")


def test_zero_amount_is_rejected():
    with pytest.raises(ValueError):
        reconstruct_swap(swap("USDC", "0", "TOKEN", "50"), "TOKEN")
