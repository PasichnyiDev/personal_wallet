from rest_framework import serializers

from .models import Wallet, Expense, Income


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = '__all__'

    def update(self, instance, validated_data):
        if ("currency" in self.initial_data) or \
           ('initial_balance' in self.initial_data) or \
           ("current_balance" in self.initial_data) or \
           ("date_created" in self.initial_data) or \
           ("is_credit_wallet" in self.initial_data) or \
           ("user" in self.initial_data):
            raise serializers.ValidationError()
        return super().update(instance, validated_data)


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
