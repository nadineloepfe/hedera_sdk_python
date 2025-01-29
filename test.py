import os
import sys
import asyncio
from dotenv import load_dotenv

from hedera_sdk_python import (
    Network,
    Client,
    AccountId,
    AccountCreateTransaction,
    PrivateKey,
    TokenCreateTransaction,
    TokenAssociateTransaction,
    TokenDissociateTransaction,
    TransferTransaction,
    TokenDeleteTransaction,
    ResponseCode,
    TopicCreateTransaction,
    TopicMessageSubmitTransaction,
    TopicUpdateTransaction,
    TopicDeleteTransaction,
    TopicId,
    TopicInfoQuery,
    CryptoGetAccountBalanceQuery,
)

load_dotenv()


def load_operator_credentials():
    """Load operator credentials from environment variables."""
    try:
        operator_id = AccountId.from_string(os.getenv('OPERATOR_ID'))
        operator_key = PrivateKey.from_string(os.getenv('OPERATOR_KEY'))
    except Exception as e:
        print(f"Error parsing operator credentials: {e}")
        sys.exit(1)
    return operator_id, operator_key


async def create_new_account(client, initial_balance=100000000):
    """
    Creates a new account with the given initial balance.

    Args:
        client (Client): The Hedera client.
        initial_balance (int): The initial balance in tinybars for the new account.

    Returns:
        (AccountId, PrivateKey): The new account's ID and its private key.
    """
    new_account_private_key = PrivateKey.generate()
    new_account_public_key = new_account_private_key.public_key()

    transaction = AccountCreateTransaction(
        key=new_account_public_key,
        initial_balance=initial_balance,
        memo="Recipient Account"
    )
    transaction.freeze_with(client)
    transaction.sign(client.operator_private_key)

    try:
        # async: call 'await'
        receipt = await transaction.execute(client)
        new_account_id = receipt.accountId
        if new_account_id is not None:
            print(f"Account creation successful. New Account ID: {new_account_id}")
            print(f"New Account Private Key: {new_account_private_key.to_string()}")
            print(f"New Account Public Key: {new_account_public_key.to_string()}")
        else:
            raise Exception("AccountID not found in receipt. Account may not have been created.")
    except Exception as e:
        print(f"Account creation failed: {str(e)}")
        sys.exit(1)

    return new_account_id, new_account_private_key


async def query_balance(client, account_id):
    """
    Queries the balance of the specified account.

    Args:
        client (Client): The Hedera client.
        account_id (AccountId): The account to check balance for.

    Returns:
        AccountBalance: The retrieved balance object (including hbars & tokens).
    """
    balance_query = CryptoGetAccountBalanceQuery(account_id=account_id)
    balance = await balance_query.execute(client)
    print(f"Account {account_id} balance: {balance.hbars}")
    return balance


async def create_token(client, operator_id, admin_key):
    """
    Creates a new token with some default parameters.

    Args:
        client (Client): The Hedera client.
        operator_id (AccountId): The treasury/account ID for the new token.
        admin_key (PrivateKey): The admin key for the token.

    Returns:
        TokenId: The ID of the newly created token.
    """
    transaction = TokenCreateTransaction(
        token_name="ExampleToken",
        token_symbol="EXT",
        decimals=2,
        initial_supply=1000,
        treasury_account_id=operator_id,
        admin_key=admin_key
    )
    transaction.freeze_with(client)
    transaction.sign(client.operator_private_key)
    transaction.sign(admin_key)

    try:
        receipt = await transaction.execute(client)
    except Exception as e:
        print(f"Token creation failed: {str(e)}")
        sys.exit(1)

    if not receipt.tokenId:
        print("Token creation failed: Token ID not returned in receipt.")
        sys.exit(1)

    token_id = receipt.tokenId
    print(f"Token creation successful. Token ID: {token_id}")
    return token_id


async def associate_token(client, recipient_id, recipient_private_key, token_ids):
    """
    Associates the specified tokens with the recipient account.
    """
    transaction = TokenAssociateTransaction(
        account_id=recipient_id,
        token_ids=token_ids
    )
    transaction.freeze_with(client)
    transaction.sign(client.operator_private_key)
    transaction.sign(recipient_private_key)

    try:
        receipt = await transaction.execute(client)
        if receipt.status != ResponseCode.SUCCESS:
            status_message = ResponseCode.get_name(receipt.status)
            raise Exception(f"Token association failed with status: {status_message}")
        print("Token association successful.")
    except Exception as e:
        print(f"Token association failed: {str(e)}")
        sys.exit(1)


async def dissociate_token(client, recipient_id, recipient_private_key, token_ids):
    """
    Dissociates the specified token(s) from the recipient account.
    """
    transaction = TokenDissociateTransaction(
        account_id=recipient_id,
        token_ids=token_ids
    )
    transaction.freeze_with(client)
    transaction.sign(client.operator_private_key)
    transaction.sign(recipient_private_key)

    try:
        receipt = await transaction.execute(client)
        if receipt.status != ResponseCode.SUCCESS:
            status_message = ResponseCode.get_name(receipt.status)
            raise Exception(f"Token dissociation failed with status: {status_message}")
        print("Token dissociation successful.")
    except Exception as e:
        print(f"Token dissociation failed: {str(e)}")
        sys.exit(1)


async def transfer_token(client, source_id, source_private_key, recipient_id, token_id):
    """
    Transfers the specified token from `source_id` to `recipient_id`.
    """
    transaction = (
        TransferTransaction()
        .add_token_transfer(token_id, source_id, -1)
        .add_token_transfer(token_id, recipient_id, 1)
        .freeze_with(client)
    )
    transaction.sign(source_private_key)

    try:
        receipt = await transaction.execute(client)
        if receipt.status != ResponseCode.SUCCESS:
            status_message = ResponseCode.get_name(receipt.status)
            raise Exception(f"Token transfer failed with status: {status_message}")
        print("Token transfer successful.")
    except Exception as e:
        print(f"Token transfer failed: {str(e)}")
        sys.exit(1)


async def delete_token(client, token_id, admin_key):
    """
    Deletes the specified token from the Hedera network.
    """
    transaction = TokenDeleteTransaction(token_id=token_id)
    transaction.freeze_with(client)
    transaction.sign(client.operator_private_key)
    transaction.sign(admin_key)

    try:
        receipt = await transaction.execute(client)
        if receipt.status != ResponseCode.SUCCESS:
            status_message = ResponseCode.get_name(receipt.status)
            raise Exception(f"Token deletion failed with status: {status_message}")
        print("Token deletion successful.")
    except Exception as e:
        print(f"Token deletion failed: {str(e)}")
        sys.exit(1)


async def create_topic(client):
    """
    Creates a new topic on the Hedera network.
    """
    key = client.operator_private_key
    transaction = TopicCreateTransaction(
        memo="Python SDK created topic",
        admin_key=key.public_key()
    )
    transaction.freeze_with(client)
    transaction.sign(key)

    try:
        receipt = await transaction.execute(client)
    except Exception as e:
        print(f"Topic creation failed: {str(e)}")
        sys.exit(1)

    if not receipt.topicId:
        print("Topic creation failed: Topic ID not returned in receipt.")
        sys.exit(1)

    topic_id = receipt.topicId
    print(f"Topic creation successful. Topic ID: {topic_id}")
    return topic_id


async def submit_message(client, topic_id):
    """
    Submits a message to the specified topic.
    """
    transaction = TopicMessageSubmitTransaction(
        topic_id=topic_id,
        message="Hello, Python SDK!"
    )
    transaction.freeze_with(client)
    transaction.sign(client.operator_private_key)

    try:
        receipt = await transaction.execute(client)
    except Exception as e:
        print(f"Message submission failed: {str(e)}")
        sys.exit(1)

    if receipt.status != ResponseCode.SUCCESS:
        status_message = ResponseCode.get_name(receipt.status)
        raise Exception(f"Message submission failed with status: {status_message}")

    print("Message submitted successfully.")


async def update_topic(client, topic_id):
    """
    Updates an existing topic with a new memo.
    """
    key = client.operator_private_key
    transaction = TopicUpdateTransaction(
        topic_id=topic_id,
        memo="Python SDK updated topic"
    )
    transaction.freeze_with(client)
    transaction.sign(key)

    try:
        receipt = await transaction.execute(client)
    except Exception as e:
        print(f"Topic update failed: {str(e)}")
        sys.exit(1)

    if receipt.status != ResponseCode.SUCCESS:
        status_message = ResponseCode.get_name(receipt.status)
        raise Exception(f"Topic update failed with status: {status_message}")

    print("Topic updated successfully.")


async def delete_topic(client, topic_id):
    """
    Deletes an existing topic from the Hedera network.
    """
    transaction = TopicDeleteTransaction(topic_id=topic_id)
    transaction.freeze_with(client)
    transaction.sign(client.operator_private_key)

    try:
        receipt = await transaction.execute(client)
    except Exception as e:
        print(f"Topic deletion failed: {str(e)}")
        sys.exit(1)

    if receipt.status != ResponseCode.SUCCESS:
        status_message = ResponseCode.get_name(receipt.status)
        raise Exception(f"Topic deletion failed with status: {status_message}")

    print("Topic deleted successfully.")


async def query_topic_info(client, topic_id):
    """
    Shows how to query topic info for an existing topic.
    """
    try:
        topic_info_query = TopicInfoQuery(topic_id=topic_id)
        topic_info = await topic_info_query.execute(client)
        print(f"Topic Info: {topic_info}")
    except Exception as e:
        print(f"Failed to retrieve topic info: {str(e)}")


async def main():
    operator_id, operator_key = load_operator_credentials()
    admin_key = PrivateKey.generate()

    network_type = os.getenv('NETWORK')
    network = Network(network=network_type)
    client = Client(network)
    client.set_operator(operator_id, operator_key)

    recipient_id, recipient_private_key = await create_new_account(client)
    await query_balance(client, recipient_id)

    token_id_1 = await create_token(client, operator_id, admin_key)
    token_id_2 = await create_token(client, operator_id, admin_key)

    await associate_token(client, recipient_id, recipient_private_key, [token_id_1, token_id_2])
    await transfer_token(client, operator_id, operator_key, recipient_id, token_id_1)
    await dissociate_token(client, recipient_id, recipient_private_key, [token_id_2])
    await delete_token(client, token_id_1, admin_key)

    topic_id = await create_topic(client)
    await submit_message(client, topic_id)
    await update_topic(client, topic_id)
    await query_topic_info(client, topic_id)
    await delete_topic(client, topic_id)


if __name__ == "__main__":
    asyncio.run(main())
