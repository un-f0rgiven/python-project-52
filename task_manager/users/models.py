from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()
    
    def __str__(self):
        return self.full_name