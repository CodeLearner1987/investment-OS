"""Conservative transaction classification.

A token transfer is NOT a buy or sell by itself. Classification requires
explicit evidence of an economic exchange (for example a DEX swap).
"""

from dataclasses import replace
from blockchain.schema.evidence import Evidence, EventType


def classify_transfer(evidence: Evidence, *, swap_detected: bool = False) -> Evidence:
    """Classify one observed transfer without inventing economic activity.

    ``swap_detected`` must come from decoded swap evidence or another trusted
    decoder. A plain ERC-20 transfer remains TRANSFER.
    """
    if not swap_detected:
        return replace(evidence, event_type=EventType.TRANSFER)

    if evidence.amount is None or evidence.counter_amount is None or not evidence.counter_asset:
        return replace(evidence, event_type=EventType.TRANSFER)

    return evidence
