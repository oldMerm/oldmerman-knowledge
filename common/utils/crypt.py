import os
import base64
import hashlib
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from typing import Union
from dotenv import load_dotenv

load_dotenv()


class AESEncryptUtil:
    """AES 对称加密工具（从环境变量读取密钥）- 静态方法版本"""

    # 类变量存储密钥
    _key = None
    _key_length = 32
    _backend = default_backend()

    @classmethod
    def _get_key(cls) -> bytes:
        """获取密钥（单例模式）"""
        if cls._key is None:
            env_key_name = "AES_SECRET_KEY"
            key = os.getenv(env_key_name)

            if key is None:
                raise ValueError(f"Environment variable {env_key_name} not found")

            key = key.encode() if isinstance(key, str) else key

            if len(key) < cls._key_length:
                key = hashlib.sha256(key).digest()
            elif len(key) > cls._key_length:
                key = key[:cls._key_length]

            cls._key = key

        return cls._key

    @staticmethod
    def _pad(data: bytes) -> bytes:
        """PKCS7 填充"""
        pad_len = 16 - (len(data) % 16)
        return data + bytes([pad_len]) * pad_len

    @staticmethod
    def _unpad(data: bytes) -> bytes:
        """去除 PKCS7 填充"""
        pad_len = data[-1]
        if pad_len < 1 or pad_len > 16:
            raise ValueError("Invalid padding")
        return data[:-pad_len]

    @classmethod
    def encrypt(cls, plaintext: Union[str, bytes]) -> str:
        """
        加密数据（类方法）

        Args:
            plaintext: 明文

        Returns:
            Base64 编码的密文（格式：IV + 密文）
        """
        if isinstance(plaintext, str):
            plaintext = plaintext.encode('utf-8')

        # 生成随机 IV（初始化向量）
        iv = os.urandom(16)

        # 获取密钥
        key = cls._get_key()

        # 创建加密器
        cipher = Cipher(
            algorithms.AES(key),
            modes.CBC(iv),
            backend=cls._backend
        )
        encryptor = cipher.encryptor()

        # 加密
        padded_data = cls._pad(plaintext)
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()

        # 返回 IV + 密文的 base64 编码
        result = base64.b64encode(iv + ciphertext).decode('utf-8')
        return result

    @classmethod
    def decrypt(cls, ciphertext: str) -> str:
        """
        解密数据（类方法）

        Args:
            ciphertext: Base64 编码的密文

        Returns:
            解密后的明文
        """
        # 解码
        raw_data = base64.b64decode(ciphertext)

        # 提取 IV 和密文
        iv = raw_data[:16]
        encrypted_data = raw_data[16:]

        # 获取密钥
        key = cls._get_key()

        # 创建解密器
        cipher = Cipher(
            algorithms.AES(key),
            modes.CBC(iv),
            backend=cls._backend
        )
        decryptor = cipher.decryptor()

        # 解密
        decrypted_padded = decryptor.update(encrypted_data) + decryptor.finalize()

        # 去除填充
        plaintext = cls._unpad(decrypted_padded)

        return plaintext.decode('utf-8')

    @staticmethod
    def generate_key(length: int = 32) -> str:
        """生成随机密钥（静态方法）"""
        import secrets
        return secrets.token_hex(length)


# 使用示例
if __name__ == "__main__":
    # 直接使用类方法，无需实例化
    data = "0+BtUHZC3GvkdR+uJbFT+1pw+5uXKI14I4VZ1jSjlTk="
    decrypted = AESEncryptUtil.decrypt(data)
    print(f"解密: {decrypted}")

    # 加密示例
    plain = "Hello World"
    encrypted = AESEncryptUtil.encrypt(plain)
    print(f"加密: {encrypted}")
    decrypted2 = AESEncryptUtil.decrypt(encrypted)
    print(f"解密: {decrypted2}")