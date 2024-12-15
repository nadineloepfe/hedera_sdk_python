from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization
from src.crypto.public_key import PublicKey

class PrivateKey:
    def __init__(self, private_key):
        self._private_key = private_key

    @classmethod
    def generate(cls):
        """
        Generates a new Ed25519 private key.

        Returns:
            PrivateKey: A new instance of PrivateKey.
        """
        private_key = ed25519.Ed25519PrivateKey.generate()
        return cls(private_key)

    @classmethod
    def from_string(cls, key_str):
        """
        Load a private key from a hex-encoded string. Supports both raw private keys (32 bytes)
        and DER-encoded private keys.
        """
        try:
            key_bytes = bytes.fromhex(key_str)
        except ValueError:
            raise ValueError("Invalid hex-encoded private key string.")

        try:
            if len(key_bytes) == 32:
                private_key = ed25519.Ed25519PrivateKey.from_private_bytes(key_bytes)
            else:
                private_key = serialization.load_der_private_key(
                    key_bytes, password=None
                )
                if not isinstance(private_key, ed25519.Ed25519PrivateKey):
                    raise TypeError("The key is not an Ed25519 private key.")
            return cls(private_key)
        except Exception as e:
            print(f"Error loading Ed25519 private key: {e}")
            raise ValueError("Failed to load private key.")

    def sign(self, data):
        """
        Signs the given data using the private key.

        Args:
            data (bytes): The data to sign.

        Returns:
            bytes: The signature.
        """
        return self._private_key.sign(data)

    def public_key(self):
        """
        Retrieves the corresponding public key.

        Returns:
            PublicKey: The public key associated with this private key.
        """
        return PublicKey(self._private_key.public_key())

    def to_string(self):
        """
        Returns the private key as a hex-encoded string.

        Returns:
            str: The hex-encoded private key.
        """
        private_bytes = self._private_key.private_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PrivateFormat.Raw,
            encryption_algorithm=serialization.NoEncryption()
        )
        return private_bytes.hex()


    def to_bytes(self):
        """
        Returns the private key as bytes.

        Returns:
            bytes: The private key.
        """
        private_bytes = self._private_key.private_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PrivateFormat.Raw,
            encryption_algorithm=serialization.NoEncryption()
        )
        return private_bytes
