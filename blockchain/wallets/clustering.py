"""Heuristic wallet clustering for economic-actor reconstruction.

Clustering is probabilistic. It must never replace raw wallet addresses or be
presented as proof of common ownership without corroborating evidence.
"""

from dataclasses import dataclass, field
from typing import Iterable


@dataclass
class WalletObservation:
    address: str
    funders: set[str] = field(default_factory=set)
    counterparties: set[str] = field(default_factory=set)
    exchange_deposits: set[str] = field(default_factory=set)
    activation_block: int | None = None


@dataclass(frozen=True)
class ClusterSignal:
    left: str
    right: str
    score: float
    reasons: tuple[str, ...]


def similarity(left: WalletObservation, right: WalletObservation) -> ClusterSignal:
    """Score shared operational fingerprints; this is not identity proof."""
    score = 0.0
    reasons: list[str] = []

    shared_funders = left.funders & right.funders
    if shared_funders:
        score += min(0.50, 0.20 * len(shared_funders))
        reasons.append("shared_funder")

    shared_counterparties = left.counterparties & right.counterparties
    if shared_counterparties:
        score += min(0.30, 0.10 * len(shared_counterparties))
        reasons.append("shared_counterparty")

    shared_exchanges = left.exchange_deposits & right.exchange_deposits
    if shared_exchanges:
        score += 0.15
        reasons.append("shared_exchange_destination")

    if left.activation_block is not None and right.activation_block is not None:
        if abs(left.activation_block - right.activation_block) <= 5:
            score += 0.05
            reasons.append("near_synchronous_activation")

    return ClusterSignal(left.address, right.address, min(score, 1.0), tuple(reasons))


def candidate_pairs(observations: Iterable[WalletObservation], threshold: float = 0.50) -> list[ClusterSignal]:
    """Return candidate pairs above a conservative threshold."""
    items = list(observations)
    signals: list[ClusterSignal] = []
    for i, left in enumerate(items):
        for right in items[i + 1:]:
            signal = similarity(left, right)
            if signal.score >= threshold:
                signals.append(signal)
    return signals
