import base64
import hashlib

from Crypto import Random
from Crypto.Cipher import AES
from django.conf import settings

class AESCipher:
    def __init__(self):
        # 블록 크기
        self.BS = 16
        # 택스트 패딩
        self.pad = lambda s: s + (self.BS - len(s) % self.BS) * chr(self.BS - len(s) % self.BS)
        self.unpad = lambda s: s[0:-s[-1]]
        # 암호화키 생성
        self.key = hashlib.sha256(settings.SECRET_KEY.encode('utf-8')).digest()

    # 암호화
    def encrypt(self, raw):
        raw = self.pad(raw).encode('utf-8')
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw))
    
    # 복호화
    def decrypt(self,enc):
        enc = base64.b64decode(enc)
        iv = enc[:16]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self.unpad(cipher.decrypt(enc[16:]))
    
    # 데이터 암호화
    def encrypt_str(self, raw):
        return self.encrypt(raw).decode('utf-8')
    
    # 데이터 복호화
    def decrypt_str(self, enc):
        if type(enc) == str:
            enc = str.encode(enc)
        return self.decrypt(enc).decode('utf-8')
    