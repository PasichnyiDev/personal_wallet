from rest_framework import serializers

from .models import Wallet, Expense, Income


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = '__all__'


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = '__all__'


class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = '__all__'


class CurrencyChoiceSerializer(serializers.Serializer):
    currency_code = serializers.CharField()
    currency_name = serializers.CharField()


class ExpensesChoiceSerializer(serializers.Serializer):
    expenses_code = serializers.CharField()
    expenses_description = serializers.CharField()


class IncomesChoiceSerializer(serializers.Serializer):
    incomes_code = serializers.CharField()
    incomes_description = serializers.CharField()
