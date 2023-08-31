from django.contrib.auth.models import AbstractUser
from django.db import models


class WalletUser(AbstractUser):
    wallets = models.ForeignKey(to='', on_delete=models.CASCADE)    # TODO

    def __str__(self) -> str:
        return self.username
