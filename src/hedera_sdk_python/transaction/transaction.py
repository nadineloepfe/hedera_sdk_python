from hedera_sdk_python.hapi.services import (
    transaction_pb2, transaction_body_pb2, basic_types_pb2,
    transaction_contents_pb2, duration_pb2
)
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat
from hedera_sdk_python.transaction.transaction_id import TransactionId

class Transaction:
    """
    Base class for all Hedera transactions.

    This class provides common functionality for building, signing, and executing transactions
    on the Hedera network. Subclasses should implement the abstract methods to define
    transaction-specific behavior.
    """

    def __init__(self):
        """
        Initializes a new Transaction instance with default values.
        """
        self.transaction_id = None
        self.node_account_id = None
        self.transaction_fee = None
        self.transaction_valid_duration = 120
        self.generate_record = False
        self.memo = ""
        self.transaction_body_bytes = None
        self.signature_map = basic_types_pb2.SignatureMap()
        self._default_transaction_fee = 2_000_000
        self.operator_account_id = None

    def sign(self, private_key):
        """
        Signs the transaction using the provided private key.

        Args:
            private_key (PrivateKey): The private key to sign the transaction with.

        Returns:
            Transaction: The current transaction instance for method chaining.

        Raises:
            Exception: If the transaction body has not been built.
        """
        if self.transaction_body_bytes is None:
            self.transaction_body_bytes = self.build_transaction_body().SerializeToString()

        signature = private_key.sign(self.transaction_body_bytes)
        public_key_bytes = private_key.public_key().to_bytes_raw()

        sig_pair = basic_types_pb2.SignaturePair(
            pubKeyPrefix=public_key_bytes,
            ed25519=signature
        )

        self.signature_map.sigPair.append(sig_pair)
        return self

    def to_proto(self):
        """
        Converts the transaction to its protobuf representation.

        Returns:
            Transaction: The protobuf Transaction message.

        Raises:
            Exception: If the transaction body has not been built.
        """
        if self.transaction_body_bytes is None:
            raise Exception("Transaction must be signed before calling to_proto()")

        signed_transaction = transaction_contents_pb2.SignedTransaction(
            bodyBytes=self.transaction_body_bytes,
            sigMap=self.signature_map
        )

        return transaction_pb2.Transaction(
            signedTransactionBytes=signed_transaction.SerializeToString()
        )

    def freeze_with(self, client):
        """
        Freezes the transaction by building the transaction body and setting necessary IDs.

        Args:
            client (Client): The client instance to use for setting defaults.

        Returns:
            Transaction: The current transaction instance for method chaining.

        Raises:
            Exception: If required IDs are not set.
        """
        if self.transaction_body_bytes is not None:
            return self

        if self.transaction_id is None:
            self.transaction_id = client.generate_transaction_id()

        if self.node_account_id is None:
            if not hasattr(client, 'node_account_id') or client.node_account_id is None:
                raise ValueError("Node account ID is not set in client.")
            self.node_account_id = client.node_account_id

        # print(f"Transaction's node account ID set to: {self.node_account_id}")
        self.transaction_body_bytes = self.build_transaction_body().SerializeToString()

        return self

    async def execute(self, client):
        """
        Executes the transaction on the Hedera network using the provided client.

        Args:
            client (Client): The client instance to use for execution.

        Returns:
            TransactionReceipt or appropriate response based on transaction type.

        Raises:
            Exception: If execution fails.
        """
        if self.transaction_body_bytes is None:
            self.freeze_with(client)

        if self.operator_account_id is None:
            self.operator_account_id = client.operator_account_id

        if not self.is_signed_by(client.operator_private_key.public_key()):
            self.sign(client.operator_private_key)

        transaction_proto = self.to_proto()
        response = await self._execute_transaction(client, transaction_proto)
        return response

    def is_signed_by(self, public_key):
        """
        Checks if the transaction has been signed by the given public key.

        Args:
            public_key (PublicKey): The public key to check.

        Returns:
            bool: True if signed by the given public key, False otherwise.
        """
        public_key_bytes = public_key.to_bytes_raw()

        for sig_pair in self.signature_map.sigPair:
            if sig_pair.pubKeyPrefix == public_key_bytes:
                return True
        return False

    def build_transaction_body(self):
        """
        Abstract method to build the transaction body.

        Subclasses must implement this method to construct the transaction-specific
        body and include it in the overall TransactionBody.

        Returns:
            TransactionBody: The protobuf TransactionBody message.

        Raises:
            NotImplementedError: Always, since subclasses must implement this method.
        """
        raise NotImplementedError("Subclasses must implement build_transaction_body()")

    def build_base_transaction_body(self):
        """
        Builds the base transaction body including common fields.

        Returns:
            TransactionBody: The protobuf TransactionBody message with common fields set.

        Raises:
            ValueError: If required IDs are not set.
        """
        if self.transaction_id is None:
            if self.operator_account_id is None:
                raise ValueError("Operator account ID is not set.")
            self.transaction_id = TransactionId.generate(self.operator_account_id)

        transaction_id_proto = self.transaction_id.to_proto()

        if self.node_account_id is None:
            raise ValueError("Node account ID is not set.")

        transaction_body = transaction_body_pb2.TransactionBody()
        transaction_body.transactionID.CopyFrom(transaction_id_proto)
        transaction_body.nodeAccountID.CopyFrom(self.node_account_id.to_proto())

        transaction_body.transactionFee = self.transaction_fee or self._default_transaction_fee
        transaction_body.transactionValidDuration.seconds = self.transaction_valid_duration
        transaction_body.generateRecord = self.generate_record
        transaction_body.memo = self.memo

        return transaction_body

    async def _execute_transaction(self, client, transaction_proto):
        """
        Abstract method to execute the transaction.

        Subclasses must implement this method to define how the transaction is sent
        to the network using the appropriate gRPC service.

        Args:
            client (Client): The client instance to use for execution.
            transaction_proto (Transaction): The protobuf Transaction message.

        Returns:
            TransactionReceipt or appropriate response based on transaction type.

        Raises:
            NotImplementedError: Always, since subclasses must implement this method.
        """
        raise NotImplementedError("Subclasses must implement _execute_transaction()")

    def _require_not_frozen(self):
        """
        Ensures the transaction is not frozen before allowing modifications.

        Raises:
            Exception: If the transaction has already been frozen.
        """
        if self.transaction_body_bytes is not None:
            raise Exception("Transaction is immutable; it has been frozen.")

    def set_transaction_memo(self, memo):
        """
        Sets the memo field for the transaction.

        Args:
            memo (str): The memo string to attach to the transaction.

        Returns:
            Transaction: The current transaction instance for method chaining.

        Raises:
            Exception: If the transaction has already been frozen.
        """
        self._require_not_frozen()
        self.memo = memo
        return self
