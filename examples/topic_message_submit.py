import os
import sys
from dotenv import load_dotenv

from hedera_sdk_python.client.client import Client
from hedera_sdk_python.account.account_id import AccountId
from hedera_sdk_python.consensus.topic_id import TopicId
from hedera_sdk_python.crypto.private_key import PrivateKey
from hedera_sdk_python.client.network import Network
from hedera_sdk_python.consensus.topic_message_submit_transaction import TopicMessageSubmitTransaction

load_dotenv()

def submit_message(message):
    network = Network(network='testnet')
    client = Client(network)

    operator_id = AccountId.from_string(os.getenv('OPERATOR_ID'))
    operator_key = PrivateKey.from_string(os.getenv('OPERATOR_KEY'))
    topic_id = TopicId.from_string(os.getenv('TOPIC_ID'))

    client.set_operator(operator_id, operator_key)

    transaction = (
        TopicMessageSubmitTransaction(topic_id=topic_id, message=message)
        .freeze_with(client)
        .sign(operator_key)
    )

    try:
        receipt = transaction.execute(client)
        print(f"Message submitted to topic {topic_id}: {message}")
    except Exception as e:
        print(f"Message submission failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    submit_message("Hello, Hedera!")