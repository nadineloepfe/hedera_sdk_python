import pytest
from src.transaction.transfer_transaction import TransferTransaction
from src.utils import generate_transaction_id

def test_add_token_transfer(mock_account_ids):
    """Test adding token transfers and ensure amounts are correctly added."""
    account_id_sender, account_id_recipient, _, token_id_1, _ = mock_account_ids
    transfer_tx = TransferTransaction()

    transfer_tx.add_token_transfer(token_id_1, account_id_sender, -100)
    transfer_tx.add_token_transfer(token_id_1, account_id_recipient, 100)

    # verify amounts were added correctly
    token_transfers = transfer_tx.token_transfers[str(token_id_1)]
    assert token_transfers[str(account_id_sender)] == -100
    assert token_transfers[str(account_id_recipient)] == 100

def test_add_hbar_transfer(mock_account_ids):
    """Test adding HBAR transfers and ensure amounts are correctly added."""
    account_id_sender, account_id_recipient, _, _, _ = mock_account_ids
    transfer_tx = TransferTransaction()

    transfer_tx.add_hbar_transfer(account_id_sender, -500)
    transfer_tx.add_hbar_transfer(account_id_recipient, 500)

    assert transfer_tx.hbar_transfers[str(account_id_sender)] == -500
    assert transfer_tx.hbar_transfers[str(account_id_recipient)] == 500

def test_add_invalid_transfer(mock_account_ids):
    """Test adding invalid transfers raises the appropriate error."""
    transfer_tx = TransferTransaction()

    with pytest.raises(TypeError):
        transfer_tx.add_hbar_transfer(12345, -500)  # invalid account_id type

    with pytest.raises(ValueError):
        transfer_tx.add_hbar_transfer(mock_account_ids[0], 0)  # invalid amount (zero)

    with pytest.raises(TypeError):
        transfer_tx.add_token_transfer(12345, mock_account_ids[0], -100)  # invalid token_id type