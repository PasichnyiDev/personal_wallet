from django.contrib.auth.models import AbstractUser
from django.db import models


class WalletUser(AbstractUser):
    date_of_birth = models.DateField(null=True, blank=True)

    def __str__(self) -> str:
        return self.email
