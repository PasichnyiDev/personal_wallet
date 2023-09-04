from django.db import models

from users.models import WalletUser


class Wallet(models.Model):

    CURRENCY_CHOICES = (
        ('USD', 'United States Dollar'),
        ('UAH', 'Ukraine Hryvnia'),
        ('EUR', 'Euro'),
        ('GBP', 'Great Britain Pound')
    )

    name = models.CharField(max_length=250)
    initial_balance = models.DecimalField(max_digits=20, decimal_places=2)
    current_balance = models.DecimalField(max_digits=20, decimal_places=2)
    currency = models.CharField(max_length=5, choices=CURRENCY_CHOICES)
    date_created = models.DateField(auto_now_add=True)
    is_credit_wallet = models.BooleanField(default=True)
    user = models.ForeignKey(to=WalletUser, on_delete=models.CASCADE)


class Expense(models.Model):

    EXPENSE_CHOICES = (
        ('FOOD', 'Food'),
        ('HOUSING', 'Housing (rent, utilities)'),
        ('TRANSPORT', 'Transport'),
        ('CLOTH', 'Cloth'),
        ('HOUSEHOLD_PR', 'Household products'),
        ('HEALTH_PR', 'Health products'),
        ('LOAN', 'Loan payments'),
        ('BILL', 'Bill payments'),
        ('INSURANCE', 'Insurance payments'),
        ('SAVE', 'Savings to the reserve fund'),
        ('OTHER', 'Other expense')
    )

    amount = models.DecimalField(max_digits=20, decimal_places=2)
    type = models.CharField(max_length=50, choices=EXPENSE_CHOICES)
    date_created = models.DateField(auto_now_add=True)
    balance_after = models.DecimalField(max_digits=20, decimal_places=2)
    wallet = models.ForeignKey(to=Wallet, on_delete=models.CASCADE)


class Income(models.Model):

    INCOME_CHOICES = (
        ('SALARY', 'Salary'),
        ('PENSION', 'Pension'),
        ('GRANT', 'Grant (scholarship)'),
        ('BENEFIT', 'Benefit'),
        ('SALES', 'Sales income'),
        ('SERVICE', 'Service income'),
        ('ROYALTY', 'Royalty'),
        ('OTHER', 'Other income')
    )

    amount = models.DecimalField(max_digits=20, decimal_places=2)
    type = models.CharField(max_length=50, choices=INCOME_CHOICES)
    date_created = models.DateField(auto_now_add=True)
    balance_after = models.DecimalField(max_digits=20, decimal_places=2)
    wallet = models.ForeignKey(to=Wallet, on_delete=models.CASCADE)
