import hashlib
import secrets
from django.db import models

class User(models.Model):
    id = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    salt = models.CharField(max_length=32, null=True)  # Assuming 32 characters for salt

    @staticmethod
    def generate_salt():
        return secrets.token_hex(16)  # Generate a random salt of 16 bytes (32 characters)

    def set_password(self, raw_password):
        self.salt = self.generate_salt()  # Generate a new salt
        hashed_password = hashlib.sha256((self.salt + raw_password).encode('utf-8')).hexdigest()
        self.password = hashed_password

    def check_password(self, raw_password):
        hashed_password = hashlib.sha256((self.salt + raw_password).encode('utf-8')).hexdigest()
        return self.password == hashed_password