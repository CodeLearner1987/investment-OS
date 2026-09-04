from datetime import datetime, timezone
from decimal import Decimal

from blockchain.decoders.erc20 import TRANSFER_TOPIC, decode_transfer
from blockchain.schema.evidence import Evidence, EventType
from blockchain.transactions.classifier import classify_transfer


def evidence() -> Evidence:
    return Evidence(
        chain="ethereum",
        tx_hash="0xabc",
        block_number=1,
        timestamp=datetime.now(timezone.utc),
        event_type=EventType.UNKNOWN,
        asset="TOKEN",
        amount=Decimal("10"),
        sender="0x1111111111111111111111111111111111111111",
        receiver="0x2222222222222222222222222222222222222222",
    )


def test_plain_transfer_is_not_a_buy():
    result = classify_transfer(evidence())
    assert result.event_type is EventType.TRANSFER


def test_swap_with_target_received_is_verified_buy():
    result = classify_transfer(
        evidence(),
        swap_detected=True,
        token_in_is_target=True,
        counter_asset="USDC",
        counter_amount=Decimal("25"),
    )
    assert result.event_type is EventType.VERIFIED_BUY
    assert result.economic_exchange()


def test_swap_with_target_spent_is_verified_sell():
    result = classify_transfer(
        evidence(),
        swap_detected=True,
        token_in_is_target=False,
        counter_asset="USDC",
        counter_amount=Decimal("25"),
    )
    assert result.event_type is EventType.VERIFIED_SELL


def test_swap_without_two_sided_evidence_stays_transfer():
    result = classify_transfer(
        evidence(), swap_detected=True, token_in_is_target=True
    )
    assert result.event_type is EventType.TRANSFER


def test_erc20_transfer_decoder():
    log = {
        "address": "0x9999999999999999999999999999999999999999",
        "topics": [
            TRANSFER_TOPIC,
            "0x0000000000000000000000001111111111111111111111111111111111111111",
            "0x0000000000000000000000002222222222222222222222222222222222222222",
        ],
        "data": hex(123456789),
        "transactionHash": "0xabc",
        "blockNumber": "0x10",
        "logIndex": "0x0",
    }
    result = decode_transfer(log, decimals=6)
    assert result is not None
    assert result.sender == "0x1111111111111111111111111111111111111111"
    assert result.receiver == "0x2222222222222222222222222222222222222222"
    assert result.raw_amount == 123456789
