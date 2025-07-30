import os
from typing import Union

from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization

from django.conf import settings


class RSAEncryption:


    def load_private_pem(self) -> bytes:
        private_pem = None
        with open(os.path.join(settings.BASE_DIR, 'nkunyim_rsa/private_key.pem'), mode='rb') as private_file:
            private_pem = private_file.read()

        return private_pem
    
    
    def load_public_pem(self, name:str) -> bytes:
        file_name = name.lower()
        public_pem = None
        with open(os.path.join(settings.BASE_DIR, f"nkunyim_rsa/{file_name}_key.pem"), mode='rb') as public_file:
            public_pem = public_file.read()

        return public_pem
    
    
    def get_private_key(self) -> rsa.RSAPrivateKey:
        private_key = serialization.load_pem_private_key(
            self.load_private_pem(),
            password=str.encode(settings.RSA_PRIVATE_PHRASE)
        )
        return private_key # type: ignore

    
    def get_public_key(self, name: Union[str, None] = None) -> rsa.RSAPublicKey:
        if name:
            public_pem = self.load_public_pem(name=name)
            public_key = serialization.load_pem_public_key(public_pem)
        else:
            private_key = self.get_private_key()
            public_key = private_key.public_key()
            
        return public_key # type: ignore
    

    def encrypt(self, plain_text: str, name: Union[str, None] = None) -> bytes:
        
        public_key = self.get_public_key(name=name)
        
        cipher_text = public_key.encrypt(
            plain_text.encode(),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        return cipher_text


    def decrypt(self, cipher_text: bytes) -> str:
        private_key = self.get_private_key()
        plain_text = private_key.decrypt(
            cipher_text,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return plain_text.decode()
