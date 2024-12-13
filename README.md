# Hedera (Mini) SDK in Python

This is a Python SDK for interacting with the Hedera Hashgraph platform. It allows developers to manage Token transactions like CREATE, ASSOCIATE and TRANSFER.


## Table of Contents

- [Installation](#installation)
- [Environment Setup](#environment-setup)
- [Running Tests](#running-tests)
- [Usage](#usage)
  - [Creating an Account](#creating-an-account)
  - [Creating a Token](#creating-a-token)
  - [Associating a Token](#associating-a-token)
  - [Transferring Tokens](#transferring-tokens)
  - [Deleting a Token](#deleting-a-token)
  - [Transferring HBAR](#transferring-hbar)
- [Contributing](#contributing)

## Installation

1. Clone this repository:

```bash
git clone https://github.com/nadineloepfe/hedera_sdk_python.git
cd hedera_sdk_python
```

2. Install dependencies:

```
pip install -r requirements.txt
```

3. Install the SDK as a Python Package:
```
pip install .
```

## Environment Setup

Before using the SDK, you need to configure your environment variables for the operator account and other credentials. Create a .env file in the root of your project with the following (replace with your environment variables):

```
OPERATOR_ID=0.0.1234xx
OPERATOR_KEY=302e020100300506032b657004220420...
ADMIN_KEY=302a300506032b65700321009308ecfdf...
RECIPIENT_ID=0.0.789xx
TOKEN_ID=0.0.100xx
```

## Running Tests

To run the test suite for the SDK, use the following command:
```
pytest ./tests 
```

The test file in the root of this project will be automatically run when pushing onto a branch.
This is done by running 'Hedera Solo'. Read more about it here:

- [Github Marketplace](https://github.com/marketplace/actions/hedera-solo)
- [Blog Post by Hendrik Ebbers](https://dev.to/hendrikebbers/ci-for-hedera-based-projects-2nja)



#### Output:
```
Account creation successful. New Account ID: 0.0.5025xxx
New Account Private Key: 228a06c363b0eb328434d51xxx...
New Account Public Key: 8f444e36e8926def492adxxx...
Token creation successful. Token ID: 0.0.5025xxx
Token association successful.
Token transfer successful.
Token deletion successful.
```


## Usage

Below are examples of how to use the SDK for creating tokens, associating them with accounts, and transferring or deleting tokens (also see 'examples' directiory)

### Creating an Account

```
transaction = (
        AccountCreateTransaction()
        .set_key(new_account_public_key)
        .set_initial_balance(initial_balance)
        .set_account_memo("Test")
        .freeze_with(client)
    )
    transaction.sign(client.operator_private_key)
    transaction.execute(client)
```


### Creating a Token

```
transaction = (
        TokenCreateTransaction()
        .set_token_name("ExampleToken")
        .set_token_symbol("EXT")
        .set_decimals(2)
        .set_initial_supply(1000)
        .set_treasury_account_id(operator_id)
        .set_admin_key(admin_key)
        .freeze_with(client)
    )

    transaction.sign(operator_key)
    transaction.execute(client)
```

### Associating a Token

```
transaction = (
        TokenAssociateTransaction()
        .set_account_id(recipient_id)
        .add_token_id(token_id)
        .freeze_with(client)
        .sign(recipient_key)
    )

    transaction.execute(client)
```

### Transfering a Token

```
    transaction = (
        TransferTransaction()
        .add_token_transfer(token_id, operator_id, -amount)
        .add_token_transfer(token_id, recipient_id, amount)
        .freeze_with(client)
        .sign(operator_key)
    )

    transaction.execute(client)
```

### Deleting a Token

```
    transaction = (
        TokenDeleteTransaction()
        .set_token_id(token_id)
        .freeze_with(client)
        .sign(operator_key)
    )
    transaction.sign(admin_key)
    transaction.execute(client)
```

### Transfering a HBAR

```
    transaction = (
        TransferTransaction()
        .add_hbar_transfer(operator_id, -100000000)  # send 1 HBAR (in tinybars)
        .add_hbar_transfer(recipient_id, 100000000)  
        .freeze_with(client)
    )

    transaction.sign(operator_key)
    transaction.execute(client)
```

## Contributing

Contributions are welcome! Please follow these steps:

    1. Fork this repository.
    2. Create a new branch with your feature or fix.
    3. Make your changes and ensure the tests pass.
    3. Submit a pull request.

Please ensure all new code is covered by unit tests.

## License

This project is licensed under the MIT License.
