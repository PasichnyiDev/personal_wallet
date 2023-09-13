from django.db.models.query import QuerySet
from django.utils import timezone
from django.db.models import Sum

from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from wallets.serializers import ExpenseSerializer, IncomeSerializer
from .serializers import TotalExpenseIncomeSerializer
from wallets.models import Expense, Income

WALLET_PARAM_KEY = "wallet_id"
TYPE_PARAM_KEY = "type"
PERIOD_PARAM_KEY = "period"


class FilterQuerySetByPeriodMixin:

    @staticmethod
    def filter_queryset_by_period(period: str, queryset: QuerySet):
        relevant_period_names = [
            "week",
            "month",
            "quarter",
            "year"
        ]
        assert period in relevant_period_names
        period_int = relevant_period_names.index(period)
        end_date = timezone.now()

        if period_int == 0:
            start_date = end_date - timezone.timedelta(days=7)
        elif period_int == 1:
            start_date = end_date - timezone.timedelta(days=30)
        elif period_int == 2:
            start_date = end_date - timezone.timedelta(days=90)
        else:
            start_date = end_date - timezone.timedelta(days=365)
        return queryset.filter(date_created__range=(start_date, end_date))


class ExpensesByTypeListView(FilterQuerySetByPeriodMixin, ListAPIView):
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        wallet_param = self.kwargs.get(WALLET_PARAM_KEY)
        type_param = self.kwargs.get(TYPE_PARAM_KEY)
        queryset = Expense.objects.filter(wallet=wallet_param).filter(type=type_param)

        # checking additional param
        period_param = self.request.query_params.get(PERIOD_PARAM_KEY)
        if period_param:
            queryset = self.filter_queryset_by_period(period=period_param, queryset=queryset)
        return queryset

    def get(self, request, *args, **kwargs):
        if self.kwargs.get(WALLET_PARAM_KEY) == self.request.user.id:
            return self.list(request, *args, **kwargs)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class IncomesByTypeListView(FilterQuerySetByPeriodMixin, ListAPIView):
    serializer_class = IncomeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        wallet_param = self.kwargs.get(WALLET_PARAM_KEY)
        type_param = self.kwargs.get(TYPE_PARAM_KEY)
        queryset = Income.objects.filter(wallet=wallet_param).filter(type=type_param)

        # checking additional param
        period_param = self.request.query_params.get(PERIOD_PARAM_KEY)
        if period_param:
            queryset = self.filter_queryset_by_period(period=period_param, queryset=queryset)
        return queryset

    def get(self, request, *args, **kwargs):
        if self.kwargs.get(WALLET_PARAM_KEY) == self.request.user.id:
            return self.list(request, *args, **kwargs)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class TotalExpensesView(FilterQuerySetByPeriodMixin, APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, wallet_id):
        wallet_param = wallet_id
        if wallet_param != self.request.user.id:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        queryset = Expense.objects.filter(wallet=wallet_param)

        # checking additional param
        period_param = request.query_params.get(PERIOD_PARAM_KEY)
        if period_param:
            queryset = self.filter_queryset_by_period(period=period_param, queryset=queryset)

        # aggregating
        total_expenses = queryset.aggregate(total=Sum('amount'))['total']
        serializer = TotalExpenseIncomeSerializer({'total': total_expenses})
        return Response(serializer.data)


class TotalIncomesView(FilterQuerySetByPeriodMixin, APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, wallet_id):
        wallet_param = wallet_id
        if wallet_param != self.request.user.id:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        queryset = Income.objects.filter(wallet=wallet_param)

        # checking additional param
        period_param = request.query_params.get(PERIOD_PARAM_KEY)
        if period_param:
            queryset = self.filter_queryset_by_period(period=period_param, queryset=queryset)

        # aggregating
        total_incomes = queryset.aggregate(total=Sum('amount'))['total']
        serializer = TotalExpenseIncomeSerializer({'total': total_incomes})
        return Response(serializer.data)
