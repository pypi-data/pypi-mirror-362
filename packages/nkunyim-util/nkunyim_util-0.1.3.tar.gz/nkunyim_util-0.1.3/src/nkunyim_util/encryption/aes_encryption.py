from cryptography.fernet import Fernet


class AESEncryption:
    
    def get_key(self) -> str:
        key = Fernet.generate_key()
        return key.decode()

    
    def encrypt(self, key: str, plain_text: str) -> str:
        cipher_suite = Fernet(key.encode())
        cipher_text = cipher_suite.encrypt(plain_text.encode())
        return cipher_text.decode()

    
    def decrypt(self, key: str, cipher_text: str) -> str:
        cipher_suite = Fernet(key.encode())
        plain_text = cipher_suite.decrypt(cipher_text.encode())
        return plain_text.decode()
