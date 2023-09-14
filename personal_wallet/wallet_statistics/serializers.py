from rest_framework import serializers


class TotalExpenseIncomeSerializer(serializers.Serializer):
    total = serializers.DecimalField(max_digits=10, decimal_places=2)


class MaxExpenseIncomeSerializer(serializers.Serializer):
    maximum = serializers.DecimalField(max_digits=10, decimal_places=2)


class ExpenseIncomePercentageSerializer(serializers.Serializer):
    type = serializers.CharField(max_length=50)
    percentage = serializers.DecimalField(max_digits=20, decimal_places=2)
