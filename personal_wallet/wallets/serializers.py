from rest_framework.serializers import ModelSerializer

from .models import Wallet, Expense, Income


class WalletSerializer(ModelSerializer):
    class Meta:
        model = Wallet
        fields = '__all__'


class ExpenseSerializer(ModelSerializer):
    class Meta:
        model = Expense
        fields = '__all__'


class IncomeSerializer(ModelSerializer):
    class Meta:
        model = Income
        fields = '__all__'

