from gmssl import sm2
from gmssl.sm4 import CryptSM4, SM4_ENCRYPT


__all__  = [
    "sm2_encrypt",
    "sm4_encrypt",
]


def sm2_encrypt(public_key: str, message: str) -> str:
    """
    SM2加密

    Args:
        public_key:
        message:

    Returns:

    """
    sm2_crypt = sm2.CryptSM2(public_key=public_key, private_key=None, mode=1)
    if isinstance(message, str):
        message = bytes(message, encoding="utf8")
    enc_data = sm2_crypt.encrypt(message)
    return enc_data.hex()


def sm4_encrypt(key: str, message: str) -> str:
    """
    SM4加密

    Args:
        key:
        message:

    Returns:

    """
    sm4 = CryptSM4()
    if isinstance(key, str):
        key = bytes(key, encoding="utf8")
    if isinstance(message, str):
        message = bytes(message, encoding="utf8")
    sm4.set_key(key, SM4_ENCRYPT)
    encrypt_value = sm4.crypt_ecb(message)
    return encrypt_value.hex()
