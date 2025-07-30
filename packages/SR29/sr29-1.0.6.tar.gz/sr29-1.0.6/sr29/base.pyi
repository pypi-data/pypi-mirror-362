import typing

__version__: str
__version_id__: int
__MAJOR__: int
__MIDLE__: int
__MINOR__: int


def require(version: str) -> int: ...


class Encrypt(object):
    code: str
    def __init__(self, fn: str, enc: typing.Union[str, bytes], salt: typing.Union[str, bytes] = 'python is fun'):
        """
        class for Encrypt data, exp `encrypt(your_data, your_password, your_salt)'
        :param fn: your source data string
        :param enc: your password
        :param salt: your salt
        """

    def hex(self) -> bytes: ...
    def hexdigest(self) -> str: ...
    def encode(self, ab: str = 'utf-8') -> bytes: ...
    def decode(self, ab: str = 'utf-8') -> str: ...


class Decrypt(object):
    deco: bytes
    def __init__(self, fn: typing.Union[str, bytes],
                 dec: typing.Union[str, bytes],
                 salt: typing.Union[str, bytes] = 'python is fun'):
        """
        class for Encrypt data, exp `Decrypt(your_data, your_password, your_salt)'

        :param fn: data encrypt
        :param dec: have password
        :param salt: optional if have salt
        """

def encrypt(fn: str, password: str, salt: str = 'python is fun') -> Encrypt:
    """
    instance of class Encrypt, exp `encrypt(your_data, your_password, your_salt)'
    :param fn: your source data string
    :param password: your password
    :param salt: your salt
    :return: Encrypt
    """


def decrypt(fn: str, dec: str, salt: str = 'python is fun') -> bytes:
    """
    instance of Decrypt class, exp `decrypt(your_data, your_password, your_salt)'

    :param fn: data encrypt
    :param dec: have password
    :param salt: optional if have salt
    """
