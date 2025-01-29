import asyncio
import time
from hedera_sdk_python.hapi.services import query_header_pb2
from hedera_sdk_python.response_code import ResponseCode
from hedera_sdk_python.hbar import Hbar
from hedera_sdk_python.transaction.transfer_transaction import TransferTransaction
from hedera_sdk_python.transaction.transaction_id import TransactionId

class Query:
    """
    Base class for all Hedera network queries.

    This class provides common functionality for constructing and executing queries
    to the Hedera network, including attaching a payment transaction if required.
    """

    def __init__(self):
        """
        Initializes the Query with default values.
        """
        self.timestamp = int(time.time())
        self.node_account_ids = []
        self.operator = None
        self.node_index = 0
        self._user_query_payment = None
        self._default_query_payment = Hbar(1)
        self.current_node_account_id = None

    def set_query_payment(self, amount: Hbar):
        """
        Allows the user to override the default query payment for queries that need to be paid.
        If not set, the default is 1 Hbar.
        """
        self._user_query_payment = amount
        return self

    def _before_execute(self, client):
        """
        Called before we execute the query. Sets up node list, operator,
        and determines if we should pay 1 Hbar by default.
        """
        if not self.node_account_ids:
            self.node_account_ids = client.get_node_account_ids()

        self.operator = self.operator or client.operator
        self.node_account_ids = list(set(self.node_account_ids))

        if self._user_query_payment is None:
            self._user_query_payment = self._default_query_payment

    def _make_request_header(self):
        """
        Constructs the request header for the query (including a payment transaction if we have an operator and node).
        """
        header = query_header_pb2.QueryHeader()
        header.responseType = query_header_pb2.ResponseType.ANSWER_ONLY

        if (
            self.operator is not None
            and self.current_node_account_id is not None
            and self._user_query_payment is not None
        ):
            payment_tx = self._build_query_payment_transaction(
                payer_account_id=self.operator.account_id,
                payer_private_key=self.operator.private_key,
                node_account_id=self.current_node_account_id,
                amount=self._user_query_payment
            )
            header.payment.CopyFrom(payment_tx)

        return header

    def _build_query_payment_transaction(self, payer_account_id, payer_private_key, node_account_id, amount: Hbar):
        """
        Uses TransferTransaction to build & sign a payment transaction for this query.
        """
        tx = TransferTransaction()
        tx.add_hbar_transfer(payer_account_id, -amount.to_tinybars())
        tx.add_hbar_transfer(node_account_id, amount.to_tinybars())

        tx.transaction_fee = 100_000_000
        tx.node_account_id = node_account_id
        tx.transaction_id = TransactionId.generate(payer_account_id)

        body_bytes = tx.build_transaction_body().SerializeToString()
        tx.transaction_body_bytes = body_bytes
        tx.sign(payer_private_key)

        return tx.to_proto()

    def _make_request(self):
        """
        Subclasses must implement to build the final query request.
        """
        raise NotImplementedError("_make_request must be implemented by subclasses.")

    def _get_status_from_response(self, response):
        """
        Subclasses must extract nodeTransactionPrecheckCode from the response.
        """
        raise NotImplementedError("_get_status_from_response must be implemented by subclasses.")

    def _map_response(self, response):
        """
        Subclasses must parse the actual data from the response.
        """
        raise NotImplementedError("_map_response must be implemented by subclasses.")

    async def execute(self, client, timeout=60):
        """
        Executes this query up to `max_attempts` times, trying different nodes if necessary.
        """
        self._before_execute(client)
        max_attempts = getattr(client, 'max_attempts', 10)

        for attempt in range(max_attempts):
            try:
                self.node_index = attempt % len(self.node_account_ids)
                self.current_node_account_id = self.node_account_ids[self.node_index]

                request = self._make_request()
                response = await client.send_query(self, self.current_node_account_id, timeout=timeout)

                if response is None:
                    continue

                status = self._get_status_from_response(response)
                if status == ResponseCode.OK:
                    return self._map_response(response)
                elif status in [ResponseCode.BUSY, ResponseCode.UNKNOWN]:
                    continue
                else:
                    from hedera_sdk_python.response_code import ResponseCode
                    raise Exception(f"Query failed with status: {ResponseCode.get_name(status)}")

            except Exception as e:
                print(f"Error executing query: {e}")
                continue

        raise Exception("Failed to execute query after maximum attempts.")
