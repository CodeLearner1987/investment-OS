"""Evidence primitives for blockchain forensic analysis.

The engine deliberately separates observed chain facts from calculated metrics
and model inferences. Raw evidence should never be overwritten by clustering
or classification.
"""

from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Any, Mapping


class EvidenceLevel(str, Enum):
    FACT = "FACT"
    CALCULATED = "CALCULATED"
    INFERRED = "INFERRED"
    UNKNOWN = "UNKNOWN"


class EventType(str, Enum):
    TRANSFER = "TRANSFER"
    VERIFIED_BUY = "VERIFIED_BUY"
    VERIFIED_SELL = "VERIFIED_SELL"
    MINT = "MINT"
    BURN = "BURN"
    LIQUIDITY_ADD = "LIQUIDITY_ADD"
    LIQUIDITY_REMOVE = "LIQUIDITY_REMOVE"
    STAKE = "STAKE"
    UNSTAKE = "UNSTAKE"
    BRIDGE = "BRIDGE"
    UNKNOWN = "UNKNOWN"


@dataclass(frozen=True)
class Evidence:
    chain: str
    tx_hash: str
    block_number: int
    timestamp: datetime
    event_type: EventType
    level: EvidenceLevel = EvidenceLevel.FACT
    asset: str | None = None
    sender: str | None = None
    receiver: str | None = None
    amount: Decimal | None = None
    counter_asset: str | None = None
    counter_amount: Decimal | None = None
    venue: str | None = None
    contract: str | None = None
    source: str = "chain"
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def economic_exchange(self) -> bool:
        """True only when the record contains both sides of an exchange."""
        return (
            self.event_type in {EventType.VERIFIED_BUY, EventType.VERIFIED_SELL}
            and self.amount is not None
            and self.counter_amount is not None
            and self.counter_asset is not None
        )
