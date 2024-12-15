from src.transaction.transaction import Transaction
from src.proto import token_create_pb2
from src.response_code import ResponseCode
from src.proto import basic_types_pb2

class TokenCreateTransaction(Transaction):
    """
    Represents a token creation transaction on the Hedera network.

    This transaction creates a new token with specified properties, such as
    name, symbol, decimals, initial supply, and treasury account.

    Inherits from the base Transaction class and implements the required methods
    to build and execute a token creation transaction.
    """

    def __init__(self):
        """
        Initializes a new TokenCreateTransaction instance with default values.
        """
        super().__init__()
        self.token_name = None
        self.token_symbol = None
        self.decimals = None
        self.initial_supply = None
        self.treasury_account_id = None
        self.admin_key = None

        self._default_transaction_fee = 3_000_000_000

    def set_token_name(self, name):
        self._require_not_frozen()
        self.token_name = name
        return self

    def set_token_symbol(self, symbol):
        self._require_not_frozen()
        self.token_symbol = symbol
        return self

    def set_decimals(self, decimals):
        self._require_not_frozen()
        self.decimals = decimals
        return self

    def set_initial_supply(self, initial_supply):
        self._require_not_frozen()
        self.initial_supply = initial_supply
        return self

    def set_treasury_account_id(self, account_id):
        self._require_not_frozen()
        self.treasury_account_id = account_id
        return self
    
    def set_admin_key(self, admin_key): 
        self._require_not_frozen()
        self.admin_key = admin_key
        return self
    
    def build_transaction_body(self):
        """
        Builds and returns the protobuf transaction body for token creation.

        Returns:
            TransactionBody: The protobuf transaction body containing the token creation details.

        Raises:
            ValueError: If required fields are missing.
        """
        if not all([
            self.token_name,
            self.token_symbol,
            self.decimals is not None,
            self.initial_supply is not None,
            self.treasury_account_id
        ]):
            raise ValueError("Missing required fields")

        key = basic_types_pb2.Key(
            ed25519=self.admin_key.to_bytes() if self.admin_key else None
        )

        token_create_body = token_create_pb2.TokenCreateTransactionBody(
            name=self.token_name,
            symbol=self.token_symbol,
            decimals=self.decimals,
            initialSupply=self.initial_supply,
            treasury=self.treasury_account_id.to_proto(),
            adminKey=key if self.admin_key else None
        )

        transaction_body = self.build_base_transaction_body()
        transaction_body.tokenCreation.CopyFrom(token_create_body)

        return transaction_body

    def _execute_transaction(self, client, transaction_proto):
        """
        Executes the token creation transaction using the provided client.

        Args:
            client (Client): The client instance to use for execution.
            transaction_proto (Transaction): The protobuf Transaction message.

        Returns:
            TransactionReceipt: The receipt from the network after transaction execution.

        Raises:
            Exception: If the transaction submission fails or receives an error response.
        """
        response = client.token_stub.createToken(transaction_proto)

        if response.nodeTransactionPrecheckCode != ResponseCode.OK:
            error_code = response.nodeTransactionPrecheckCode
            error_message = ResponseCode.get_name(error_code)
            raise Exception(f"Error during transaction submission: {error_code} ({error_message})")

        receipt = self.get_receipt(client)
        return receipt

    def get_receipt(self, client, timeout=60):
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
        
        receipt = client.get_transaction_receipt(self.transaction_id, timeout)
        return receipt
