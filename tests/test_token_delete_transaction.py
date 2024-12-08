import pytest
from unittest.mock import MagicMock
from src.tokens.token_delete_transaction import TokenDeleteTransaction
from src.proto import basic_types_pb2, timestamp_pb2
from src.transaction.transaction_id import TransactionId

def generate_transaction_id(account_id_proto):
    """Generate a unique transaction ID based on the account ID and the current timestamp."""
    import time
    current_time = time.time()
    timestamp_seconds = int(current_time)
    timestamp_nanos = int((current_time - timestamp_seconds) * 1e9)

    tx_timestamp = timestamp_pb2.Timestamp(seconds=timestamp_seconds, nanos=timestamp_nanos)

    tx_id = TransactionId(
        valid_start=tx_timestamp,
        account_id=account_id_proto
    )
    return tx_id

def test_build_transaction_body(mock_account_ids):
    """Test building a token delete transaction body with a valid value."""
    operator_id, _, node_account_id, token_id, _= mock_account_ids

    delete_tx = TokenDeleteTransaction()
    delete_tx.set_token_id(token_id)
    delete_tx.transaction_id = generate_transaction_id(operator_id)
    delete_tx.node_account_id = node_account_id

    transaction_body = delete_tx.build_transaction_body()

    assert transaction_body.tokenDeletion.token.shardNum == 1
    assert transaction_body.tokenDeletion.token.realmNum == 1
    assert transaction_body.tokenDeletion.token.tokenNum == 1

def test_missing_token_id():
    """Test that building a transaction without setting TokenID raises a ValueError."""
    delete_tx = TokenDeleteTransaction()
    with pytest.raises(ValueError, match="Missing required TokenID."):
        delete_tx.build_transaction_body()

def test_sign_transaction(mock_account_ids):
    """Test signing the token delete transaction with a private key."""
    operator_id, _, node_account_id, token_id, _= mock_account_ids
    delete_tx = TokenDeleteTransaction()
    delete_tx.set_token_id(token_id)
    delete_tx.transaction_id = generate_transaction_id(operator_id)
    delete_tx.node_account_id = node_account_id

    private_key = MagicMock()
    private_key.sign.return_value = b'signature'
    private_key.public_key().public_bytes.return_value = b'public_key'

    delete_tx.sign(private_key)

    assert len(delete_tx.signature_map.sigPair) == 1
    sig_pair = delete_tx.signature_map.sigPair[0]
    assert sig_pair.pubKeyPrefix == b'public_key'
    assert sig_pair.ed25519 == b'signature'


def test_to_proto(mock_account_ids):
    """Test converting the token delete transaction to protobuf format after signing."""
    operator_id, _, node_account_id, token_id, _= mock_account_ids
    delete_tx = TokenDeleteTransaction()
    delete_tx.set_token_id(token_id)
    delete_tx.transaction_id = generate_transaction_id(operator_id)
    delete_tx.node_account_id = node_account_id

    private_key = MagicMock()
    private_key.sign.return_value = b'signature'
    private_key.public_key().public_bytes.return_value = b'public_key'

    delete_tx.sign(private_key)
    proto = delete_tx.to_proto()

    assert proto.signedTransactionBytes
    assert len(proto.signedTransactionBytes) > 0
