from django.contrib.auth.models import AbstractUser


class WalletUser(AbstractUser):
    pass

    def __str__(self) -> str:
        return self.username
