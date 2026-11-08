"""Tests for PII masking at the API boundary."""

from api.pii import MASK, mask_pii


def test_mask_pii_masks_email_phone_card_and_account_sequences() -> None:
    raw = "jane@example.com 0412345678 4111 1111 1111 1111 account 12345678"

    masked = mask_pii(raw)

    assert masked.count(MASK) == 4
    for value in ("jane@example.com", "0412345678", "4111 1111 1111 1111", "12345678"):
        assert value not in masked
