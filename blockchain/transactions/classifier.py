"""Conservative economic-event classifier.

A token movement is never upgraded to BUY/SELL merely because a transfer exists.
The caller must provide decoded two-sided swap evidence.
"""

from __future__ import annotations

from dataclasses import replace
from typing import Any

from blockchain.schema.evidence import Evidence, EventType


def classify_transfer(
    evidence: Evidence,
    *,
    swap_detected: bool = False,
    token_in_is_target: bool | None = None,
    counter_asset: str | None = None,
    counter_amount: Any = None,
) -> Evidence:
    """Classify an observed movement without manufacturing economic evidence.

    BUY means the target asset was received while a counter asset was spent.
    SELL means the target asset was spent while a counter asset was received.
    Anything less remains TRANSFER.
    """
    if not swap_detected or token_in_is_target is None:
        return replace(evidence, event_type=EventType.TRANSFER)
    if counter_asset is None or counter_amount is None or evidence.amount is None:
        return replace(evidence, event_type=EventType.TRANSFER)

    event_type = EventType.VERIFIED_BUY if token_in_is_target else EventType.VERIFIED_SELL
    return replace(
        evidence,
        event_type=event_type,
        counter_asset=counter_asset,
        counter_amount=counter_amount,
    )
