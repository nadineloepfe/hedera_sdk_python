from hedera_sdk_python.query.query import Query
from hedera_sdk_python.hapi.services import crypto_get_account_balance_pb2, query_pb2
from hedera_sdk_python.account.account_id import AccountId
from hedera_sdk_python.account.account_balance import AccountBalance


class CryptoGetAccountBalanceQuery(Query):
    """
    A query to retrieve the balance of a specific account from the Hedera network.

    This class constructs and executes a query to obtain the balance of an account,
    including hbars and tokens.
    """

    def __init__(self, account_id: AccountId = None):
        """
        Initializes a new instance of the CryptoGetAccountBalanceQuery class.

        Args:
            account_id (AccountId, optional): The ID of the account to retrieve the balance for.
        """
        super().__init__()
        self.account_id = account_id

    def set_account_id(self, account_id: AccountId):
        """
        Sets the account ID for which to retrieve the balance.

        Args:
            account_id (AccountId): The ID of the account.

        Returns:
            CryptoGetAccountBalanceQuery: The current instance for method chaining.
        """
        self.account_id = account_id
        return self

    def _make_request(self):
        """
        Constructs the protobuf request for the account balance query.

        Returns:
            Query: The protobuf Query object containing the account balance query.

        Raises:
            ValueError: If the account ID is not set.
            Exception: If an error occurs during request construction.
        """
        try:
            if not self.account_id:
                raise ValueError("Account ID must be set before making the request.")

            query_header = self._make_request_header()
            crypto_get_balance = crypto_get_account_balance_pb2.CryptoGetAccountBalanceQuery()
            crypto_get_balance.header.CopyFrom(query_header)
            crypto_get_balance.accountID.CopyFrom(self.account_id.to_proto())

            query = query_pb2.Query()
            if not hasattr(query, 'cryptogetAccountBalance'):
                raise AttributeError("Query object has no attribute 'cryptogetAccountBalance'")
            query.cryptogetAccountBalance.CopyFrom(crypto_get_balance)

            return query
        except Exception as e:
            print(f"Exception in _make_request: {e}")
            import traceback
            traceback.print_exc()
            raise

    def _get_status_from_response(self, response):
        """
        Extracts the status code from the response header.

        Args:
            response (Response): The response received from the network.

        Returns:
            int: The status code indicating the result of the query.
        """
        header = response.cryptogetAccountBalance.header
        return header.nodeTransactionPrecheckCode

    def _map_response(self, response):
        """
        Maps the response to an AccountBalance object.

        Args:
            response (Response): The response received from the network.

        Returns:
            AccountBalance: The account balance extracted from the response.

        Raises:
            Exception: If the account balance is not found in the response.
        """
        if response.cryptogetAccountBalance:
            balance_proto = response.cryptogetAccountBalance
            return AccountBalance.from_proto(balance_proto)
        else:
            raise Exception("Account balance not found in the response.")

    async def execute(self, client):
        """
        Executes the account balance query against the provided client asynchronously.

        Args:
            client (Client): The async client to use for sending the query.

        Returns:
            AccountBalance: The account balance extracted from the network response.

        Raises:
            Exception: If any precheck failure or network error occurs.
        """
        request = self._make_request()
        response = await client.send_query(self, client.node_account_id)
        precheck_code = self._get_status_from_response(response)
        if precheck_code != 0:  # e.g. 0 = SUCCESS
            from hedera_sdk_python.response_code import ResponseCode
            code_name = ResponseCode.get_name(precheck_code)
            raise Exception(f"Precheck failed with code {code_name} ({precheck_code})")

        return self._map_response(response)
