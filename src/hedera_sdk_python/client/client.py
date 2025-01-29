import asyncio
from collections import namedtuple

import grpc.aio
from hedera_sdk_python.hapi.services import (
    consensus_service_pb2_grpc,
    token_service_pb2_grpc,
    crypto_service_pb2_grpc
)

from hedera_sdk_python.hapi.mirror import (
    consensus_service_pb2_grpc as mirror_consensus_grpc,
    mirror_network_service_pb2_grpc as mirror_network_grpc
)

from .network import Network
from hedera_sdk_python.response_code import ResponseCode
from hedera_sdk_python.query.transaction_get_receipt_query import TransactionGetReceiptQuery
from hedera_sdk_python.transaction.transaction_id import TransactionId

Operator = namedtuple('Operator', ['account_id', 'private_key'])

class Client:
    """
    Represents a client to interact with the Hedera network.
    """

    def __init__(self, network=None):
        self.operator_account_id = None
        self.operator_private_key = None

        if network is None:
            network = Network()
        self.network = network

        self.channel = None
        self.token_stub = None
        self.crypto_stub = None
        self.topic_stub = None
        self.mirror_channel = None
        self.mirror_stub = None

        self.max_attempts = 10 

        node_account_ids = self.get_node_account_ids()
        if not node_account_ids:
            raise ValueError("No nodes available in the network configuration.")

        initial_node_id = node_account_ids[0]
        self._switch_node(initial_node_id)

        self._init_mirror_stub()

    def _init_mirror_stub(self):
        """
        Connect to a mirror node for topic message subscriptions.
        For testnet, we can use a known address like:
            hcs.testnet.mirrornode.hedera.com:5600
        """
        mirror_address = self.network.get_mirror_address()
        self.mirror_channel = grpc.aio.insecure_channel(mirror_address)
        self.mirror_stub = mirror_consensus_grpc.ConsensusServiceStub(self.mirror_channel)

    def set_operator(self, account_id, private_key):
        self.operator_account_id = account_id
        self.operator_private_key = private_key

    @property
    def operator(self):
        if self.operator_account_id is not None and self.operator_private_key is not None:
            return Operator(account_id=self.operator_account_id, private_key=self.operator_private_key)
        else:
            return None

    def generate_transaction_id(self):
        if self.operator_account_id is None:
            raise ValueError("Operator account ID must be set to generate transaction ID.")
        return TransactionId.generate(self.operator_account_id)

    def get_node_account_ids(self):
        """
        Returns a list of node AccountIds that the client can use to send queries and transactions.

        Returns:
            list: A list of AccountId instances representing the nodes.
        """
        if self.network and self.network.nodes:
            return [account_id for (address, account_id) in self.network.nodes]
        else:
            raise ValueError("No nodes available in the network configuration.")

    async def get_transaction_receipt(self, transaction_id, max_attempts=10, sleep_seconds=2):
        for attempt in range(max_attempts):
            try:
                receipt_query = TransactionGetReceiptQuery()
                receipt_query.set_transaction_id(transaction_id)
                receipt = await receipt_query.execute(self)  
                status = receipt.status

                if status == ResponseCode.SUCCESS:
                    return receipt
                elif status in (ResponseCode.UNKNOWN, ResponseCode.RECEIPT_NOT_FOUND):
                    await asyncio.sleep(sleep_seconds)
                    continue
                else:
                    status_message = ResponseCode.get_name(status)
                    raise Exception(f"Transaction failed with status: {status_message}")
            except Exception as e:
                print(f"Error retrieving transaction receipt: {e}")
                await asyncio.sleep(sleep_seconds)
        raise Exception("Exceeded maximum attempts to fetch transaction receipt.")

    async def send_query(self, query, node_account_id, timeout=60):
        """
        Sends a query to the specified node and returns the response.

        Args:
            query (Query): The query to send.
            node_account_id (AccountId): The node account ID to send the query to.
            timeout (int, optional): Timeout for the query in seconds. Defaults to 60.

        Returns:
            Response: The response from the network.

        Raises:
            None. Exceptions are caught and printed, returning None on failure.
        """
        self._switch_node(node_account_id)

        try:
            request = query._make_request()

            if hasattr(request, 'cryptogetAccountBalance'):
                response = await self.crypto_stub.cryptoGetBalance(request, timeout=timeout)
            elif hasattr(request, 'transactionGetReceipt'):
                response = await self.crypto_stub.getTransactionReceipts(request, timeout=timeout)
            elif hasattr(request, 'consensusGetTopicInfo'):
                response = await self.topic_stub.getTopicInfo(request, timeout=timeout)
            else:
                raise Exception("Unsupported query type.")
            return response

        except grpc.aio.AioRpcError as e:
            print(f"gRPC error during query execution: {e}")
            return None

    def _switch_node(self, node_account_id):
        """
        Switches to the specified node in the network and updates the gRPC stubs.

        Args:
            node_account_id (AccountId): The account ID of the node to switch to.

        Raises:
            ValueError: If the node account ID is not found in the network configuration.
        """
        node_address = self.network.get_node_address(node_account_id)
        if node_address is None:
            raise ValueError(f"No node address found for account ID {node_account_id}")

        self.channel = grpc.aio.insecure_channel(node_address)
        self.token_stub = token_service_pb2_grpc.TokenServiceStub(self.channel)
        self.crypto_stub = crypto_service_pb2_grpc.CryptoServiceStub(self.channel)
        self.topic_stub = consensus_service_pb2_grpc.ConsensusServiceStub(self.channel)
        self.node_account_id = node_account_id
