import pytest
from src.account.account_id import AccountId
from src.tokens.token_id import TokenId
from src.crypto.private_key import PrivateKey
from cryptography.hazmat.primitives import serialization

@pytest.fixture
def mock_account_ids():
    """Fixture to provide mock account IDs and token IDs."""
    account_id_sender = AccountId(0, 0, 1)
    account_id_recipient = AccountId(0, 0, 2)
    node_account_id = AccountId(0, 0, 3)
    token_id_1 = TokenId(1, 1, 1)
    token_id_2 = TokenId(2, 2, 2)
    return account_id_sender, account_id_recipient, node_account_id, token_id_1, token_id_2

@pytest.fixture
def admin_key():
    admin_key = PrivateKey.generate()

    admin_public_key_bytes = admin_key.public_key().public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw
    )

    return admin_key, admin_public_key_bytes
