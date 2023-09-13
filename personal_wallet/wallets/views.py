from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

from users.models import WalletUser
from .models import Wallet, Expense, Income
from .serializers import WalletSerializer, ExpenseSerializer, IncomeSerializer, \
                         CurrencyChoiceSerializer, ExpensesChoiceSerializer, IncomesChoiceSerializer
from .choices import CURRENCY_CHOICES, EXPENSES_CHOICES, INCOMES_CHOICES

REQUEST_GET = 'GET'

ID_KEY = 'id'
WALLET_KEY = 'wallet'
WALLETS_KEY = 'wallets'
WALLET_NAME_KEY = 'name'
WALLET_INITIAL_BALANCE_KEY = 'initial_balance'
WALLET_CURRENT_BALANCE_KEY = 'current_balance'
WALLET_CURRENCY_KEY = 'currency'
WALLET_IS_CREDIT_WALLET_KEY = 'is_credit_wallet'
WALLET_USER_KEY = 'user'
WALLET_ID_KEY = 'wallet_id'

EXPENSE_KEY = 'expense'
EXPENSES_KEY = 'expenses'
EXPENSE_ID_KEY = 'expense_id'

INCOME_KEY = 'income'
INCOMES_KEY = 'incomes'
INCOME_ID_KEY = 'income_id'

EXPENSE_INCOME_AMOUNT_KEY = 'amount'
EXPENSE_INCOME_TYPE_KEY = 'type'
EXPENSE_INCOME_BALANCE_AFTER_KEY = 'balance_after'
EXPENSE_INCOME_DATE_CREATED_KEY = 'date_created'
DATE_FORMAT = '%Y-%d-%m'

JS_FALSE = 'false'
JS_TRUE = 'true'

MESSAGE_KEY = 'message'


class WalletViewSet(viewsets.ModelViewSet):

    permission_classes = [IsAuthenticated]
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    lookup_url_kwarg = WALLET_ID_KEY

    def create(self, request, *args, **kwargs):

        user = WalletUser.objects.get(username=request.user.username)
        name = request.data.get(WALLET_NAME_KEY)
        initial_balance = request.data.get(WALLET_INITIAL_BALANCE_KEY)
        if float(initial_balance) < 0:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        current_balance = initial_balance
        currency = request.data.get(WALLET_CURRENCY_KEY)
        is_credit_wallet = False if request.data.get(WALLET_IS_CREDIT_WALLET_KEY) == JS_FALSE else True

        serializer = WalletSerializer(
            data={
                WALLET_NAME_KEY: name,
                WALLET_INITIAL_BALANCE_KEY: initial_balance,
                WALLET_CURRENT_BALANCE_KEY: current_balance,
                WALLET_CURRENCY_KEY: currency,
                WALLET_IS_CREDIT_WALLET_KEY: is_credit_wallet,
                WALLET_USER_KEY: user.pk
            }
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({MESSAGE_KEY: 'Success'}, status=status.HTTP_204_NO_CONTENT)

    def list(self, request, *args, **kwargs):
        return Response(WalletSerializer(Wallet.objects.filter(user=request.user.pk), many=True).data)


class ExpenseViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):

    def create(self, request, *args, **kwargs):

        expense_amount = request.data.get(EXPENSE_INCOME_AMOUNT_KEY)
        if float(expense_amount) <= 0:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        expense_type = request.data.get(EXPENSE_INCOME_TYPE_KEY)
        date_created = request.data.get(EXPENSE_INCOME_DATE_CREATED_KEY)
        if not date_created:
            date_created = timezone.now().date()
        wallet = Wallet.objects.get(id=kwargs.get(WALLET_ID_KEY))
        if wallet.user.id != request.user.pk:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        possible_balance = float(wallet.current_balance) - float(expense_amount)
        if not wallet.is_credit_wallet and possible_balance < 0:
            return Response(
                {MESSAGE_KEY: 'Too big expense amount for not credit wallet'},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )
        else:
            wallet.current_balance = round(possible_balance, 2)
            balance_after = round(possible_balance, 2)
            serializer = ExpenseSerializer(
                data={
                    EXPENSE_INCOME_AMOUNT_KEY: expense_amount,
                    EXPENSE_INCOME_TYPE_KEY: expense_type,
                    EXPENSE_INCOME_BALANCE_AFTER_KEY: balance_after,
                    EXPENSE_INCOME_DATE_CREATED_KEY: date_created,
                    WALLET_KEY: wallet.id
                }
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            wallet.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        try:
            expense_instance = Expense.objects.get(id=kwargs.get(EXPENSE_ID_KEY))
            wallet_instance = Wallet.objects.get(id=kwargs.get(WALLET_ID_KEY))
            if wallet_instance.user.id != request.user.pk:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        wallet_instance.current_balance = round(
            float(wallet_instance.current_balance) + float(expense_instance.amount), 2
        )
        wallet_instance.save()
        expense_instance.delete()
        return Response({MESSAGE_KEY: 'Success'}, status=status.HTTP_204_NO_CONTENT)

    def list(self, request, *args, **kwargs):
        return Response(
            {EXPENSES_KEY: ExpenseSerializer(Expense.objects.filter(wallet=kwargs.get(WALLET_ID_KEY)), many=True).data}
        )


class IncomeViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):

    def create(self, request, *args, **kwargs):
        income_amount = request.data.get(EXPENSE_INCOME_AMOUNT_KEY)
        if float(income_amount) <= 0:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        income_type = request.data.get(EXPENSE_INCOME_TYPE_KEY)
        date_created = request.data.get(EXPENSE_INCOME_DATE_CREATED_KEY)
        if not date_created:
            date_created = timezone.now().date()
        wallet = Wallet.objects.get(id=kwargs.get(WALLET_ID_KEY))
        if wallet.user.id != request.user.pk:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        wallet.current_balance = round(float(wallet.current_balance) + float(income_amount), 2)
        balance_after = wallet.current_balance
        serializer = IncomeSerializer(
            data={
                EXPENSE_INCOME_AMOUNT_KEY: income_amount,
                EXPENSE_INCOME_TYPE_KEY: income_type,
                EXPENSE_INCOME_BALANCE_AFTER_KEY: balance_after,
                EXPENSE_INCOME_DATE_CREATED_KEY: date_created,
                WALLET_KEY: wallet.id
            }
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        wallet.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        try:
            income_instance = Income.objects.get(id=kwargs.get(INCOME_ID_KEY))
            wallet_instance = Wallet.objects.get(id=kwargs.get(WALLET_ID_KEY))
            if wallet_instance.user.id != request.user.pk:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if not wallet_instance.is_credit_wallet and (wallet_instance.current_balance - income_instance.amount < 0):
            return Response(
                {MESSAGE_KEY: 'Cannot delete this income, because this wallet is not credit'},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )

        wallet_instance.current_balance = round(
            float(wallet_instance.current_balance) - float(income_instance.amount), 2
        )
        wallet_instance.save()
        income_instance.delete()
        return Response({MESSAGE_KEY: 'Success'}, status=status.HTTP_204_NO_CONTENT)

    def list(self, request, *args, **kwargs):
        return Response(
            {INCOMES_KEY: IncomeSerializer(Income.objects.filter(wallet=kwargs.get(WALLET_ID_KEY)), many=True).data}
        )


@api_view([REQUEST_GET])
def get_expenses_choices(request):
    expenses_choices = [
        {'expenses_code': code, 'expenses_description': description}
        for code, description in EXPENSES_CHOICES
    ]
    serializer = ExpensesChoiceSerializer(expenses_choices, many=True)
    return Response(serializer.data)


@api_view([REQUEST_GET])
def get_incomes_choices(request):
    incomes_choices = [
        {'incomes_code': code, 'incomes_description': description}
        for code, description in INCOMES_CHOICES
    ]
    serializer = IncomesChoiceSerializer(incomes_choices, many=True)
    return Response(serializer.data)


@api_view([REQUEST_GET])
def get_currency_choices(request):
    currency_choices = [
        {'currency_code': code, 'currency_name': name}
        for code, name in CURRENCY_CHOICES
    ]
    serializer = CurrencyChoiceSerializer(currency_choices, many=True)
    return Response(serializer.data)
