from django.db import models

from users.models import WalletUser
from .choices import CURRENCY_CHOICES, EXPENSES_CHOICES, INCOMES_CHOICES


class Wallet(models.Model):

    name = models.CharField(max_length=250)
    initial_balance = models.DecimalField(max_digits=20, decimal_places=2)
    current_balance = models.DecimalField(max_digits=20, decimal_places=2)
    currency = models.CharField(max_length=5, choices=CURRENCY_CHOICES)
    date_created = models.DateField(auto_now_add=True)
    is_credit_wallet = models.BooleanField(default=True)
    user = models.ForeignKey(to=WalletUser, on_delete=models.CASCADE)


class Expense(models.Model):

    amount = models.DecimalField(max_digits=20, decimal_places=2)
    type = models.CharField(max_length=50, choices=EXPENSES_CHOICES)
    date_created = models.DateField(auto_now_add=True)
    balance_after = models.DecimalField(max_digits=20, decimal_places=2)
    wallet = models.ForeignKey(to=Wallet, on_delete=models.CASCADE)


class Income(models.Model):

    amount = models.DecimalField(max_digits=20, decimal_places=2)
    type = models.CharField(max_length=50, choices=INCOMES_CHOICES)
    date_created = models.DateField(auto_now_add=True)
    balance_after = models.DecimalField(max_digits=20, decimal_places=2)
    wallet = models.ForeignKey(to=Wallet, on_delete=models.CASCADE)
