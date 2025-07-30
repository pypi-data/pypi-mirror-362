import base64

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


class AESCipher:
    def __init__(self, key, iv):
        self.key = key
        self.iv = iv

    def __new__(cls, *args, **kwargs):
        """单例模式，作为被config导入的类，就不导入元类单例实现了，尽量避免不必要的问题"""
        if not hasattr(cls, "_instance"):
            cls._instance = super(AESCipher, cls).__new__(cls)
        return cls._instance

    def encrypt(self, plaintext: str, key: str = None, iv: str = None) -> str:
        """AES加密（返回Base64编码的字符串）"""
        key, iv = key or self.key, iv or self.iv
        cipher = AES.new(key.encode("utf8"), AES.MODE_CBC, iv.encode("utf8"))
        padded_data = pad(plaintext.encode("utf-8"), AES.block_size)
        encrypted = cipher.encrypt(padded_data)
        return base64.b64encode(encrypted).decode("utf-8")

    def decrypt(self, encrypted_b64: str, key: str = None, iv: str = None) -> str:
        """AES解密（输入Base64编码的字符串）"""
        key, iv = key or self.key, iv or self.iv
        encrypted = base64.b64decode(encrypted_b64)
        cipher = AES.new(key.encode("utf8"), AES.MODE_CBC, iv.encode("utf8"))
        decrypted = cipher.decrypt(encrypted)
        return unpad(decrypted, AES.block_size).decode("utf-8")

    def encrypt_db(self, data: dict):
        for k, v in data.items():
            if isinstance(v, str):
                data[k] = self.encrypt(v, self.key, self.iv)
            elif isinstance(v, dict):
                self.encrypt_db(v)

    def decrypt_db(self, data: dict):
        for k, v in data.items():
            if isinstance(v, str):
                try:
                    data[k] = self.decrypt(v, self.key, self.iv)
                except ValueError:
                    pass
            elif isinstance(v, dict):
                self.decrypt_db(v)


# 示例使用
if __name__ == "__main__":
    original = "Hello, AES加密测试！"

    # # 固定参数（必须为16/24/32字节长度）
    KEY = "this_is_a_32byte_key_for_aes_256"  # 32字节（256位）
    IV = "qa250513autotest"  # 16字节（必须）
    aes = AESCipher(KEY, IV)
    aes1 = AESCipher(KEY, IV)
    # 加密
    encrypted = aes.encrypt(original)
    print("加密结果 (Base64):", encrypted)
    # 解密
    decrypted = aes.decrypt(encrypted)
    print("解密结果:", decrypted)
