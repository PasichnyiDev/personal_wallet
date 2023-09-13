from rest_framework import serializers


class TotalExpenseIncomeSerializer(serializers.Serializer):
    total = serializers.DecimalField(max_digits=10, decimal_places=2)
