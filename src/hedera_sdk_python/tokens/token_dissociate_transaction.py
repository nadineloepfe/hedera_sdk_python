from hedera_sdk_python.transaction.transaction import Transaction
from hedera_sdk_python.hapi.services import token_dissociate_pb2
from hedera_sdk_python.response_code import ResponseCode

class TokenDissociateTransaction(Transaction):
    """
    Represents a token dissociate transaction on the Hedera network.

    This transaction dissociates the specified tokens with an account,
    meaning the account can no longer hold or transact with those tokens.

    Inherits from the base Transaction class and implements the required methods
    to build and execute a token dissociate transaction.
    """

    def __init__(self, account_id=None, token_ids=None):
        """
        Initializes a new TokenDissociateTransaction instance with default values.
        """
        super().__init__()
        self.account_id = account_id
        self.token_ids = token_ids or []

        self._default_transaction_fee = 500_000_000

    def set_account_id(self, account_id):
        self._require_not_frozen()
        self.account_id = account_id
        return self

    def add_token_id(self, token_id):
        self._require_not_frozen()
        self.token_ids.append(token_id)
        return self

    def build_transaction_body(self):
        """
        Builds and returns the protobuf transaction body for token dissociation.

        Returns:
            TransactionBody: The protobuf transaction body containing the token dissociation details.

        Raises:
            ValueError: If account ID or token IDs are not set.
        """
        if not self.account_id or not self.token_ids:
            raise ValueError("Account ID and token IDs must be set.")

        token_dissociate_body = token_dissociate_pb2.TokenDissociateTransactionBody(
            account=self.account_id.to_proto(),
            tokens=[token_id.to_proto() for token_id in self.token_ids]
        )

        transaction_body = self.build_base_transaction_body()
        transaction_body.tokenDissociate.CopyFrom(token_dissociate_body)
    
        return transaction_body

    async def _execute_transaction(self, client, transaction_proto):
        """
        Executes the token dissociation transaction using the provided client.

        Args:
            client (Client): The client instance to use for execution.
            transaction_proto (Transaction): The protobuf Transaction message.

        Returns:
            TransactionReceipt: The receipt from the network after transaction execution.

        Raises:
            Exception: If the transaction submission fails or receives an error response.
        """
        response = await client.token_stub.dissociateTokens(transaction_proto)

        if response.nodeTransactionPrecheckCode != ResponseCode.OK:
            error_code = response.nodeTransactionPrecheckCode
            error_message = ResponseCode.get_name(error_code)
            raise Exception(f"Error during transaction submission: {error_code} ({error_message})")

        receipt = await self.get_receipt(client)
        return receipt

    async def get_receipt(self, client, timeout=60):
        """
        Retrieves the receipt for the transaction.

        Args:
            client (Client): The client instance.
            timeout (int): Maximum time in seconds to wait for the receipt.

        Returns:
            TransactionReceipt: The transaction receipt from the network.

        Raises:
            Exception: If the transaction ID is not set or if receipt retrieval fails.
        """
        if self.transaction_id is None:
            raise Exception("Transaction ID is not set.")

        return await client.get_transaction_receipt(self.transaction_id, timeout)
