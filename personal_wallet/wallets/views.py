from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_422_UNPROCESSABLE_ENTITY, \
    HTTP_400_BAD_REQUEST

from users.models import WalletUser
from .models import Wallet, Expense, Income
from .serializers import WalletSerializer, ExpenseSerializer, IncomeSerializer

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
        return Response(serializer.data, status=HTTP_201_CREATED, headers=headers)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({MESSAGE_KEY: 'Success'}, status=HTTP_204_NO_CONTENT)

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
        expense_type = request.data.get(EXPENSE_INCOME_TYPE_KEY)
        wallet = Wallet.objects.get(id=kwargs.get(WALLET_ID_KEY))

        possible_balance = wallet.current_balance - float(expense_amount)
        if not wallet.is_credit_wallet and possible_balance < 0:
            return Response(
                {MESSAGE_KEY: 'Too big expense amount for not credit wallet'}, status=HTTP_422_UNPROCESSABLE_ENTITY
            )
        else:
            wallet.current_balance = possible_balance
            balance_after = possible_balance
            serializer = ExpenseSerializer(
                data={
                    EXPENSE_INCOME_AMOUNT_KEY: expense_amount,
                    EXPENSE_INCOME_TYPE_KEY: expense_type,
                    EXPENSE_INCOME_BALANCE_AFTER_KEY: balance_after,
                    WALLET_KEY: wallet
                }
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({EXPENSE_KEY: serializer.data}, status=HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        instance = Expense.objects.get(id=kwargs.get(EXPENSE_ID_KEY))
        instance.delete()
        return Response({MESSAGE_KEY: 'Success'}, status=HTTP_204_NO_CONTENT)

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
        income_type = request.data.get(EXPENSE_INCOME_TYPE_KEY)
        wallet = Wallet.objects.get(id=kwargs.get(WALLET_ID_KEY))

        wallet.current_balance += float(income_amount)
        balance_after = wallet.current_balance
        serializer = ExpenseSerializer(
            data={
                EXPENSE_INCOME_AMOUNT_KEY: income_amount,
                EXPENSE_INCOME_TYPE_KEY: income_type,
                EXPENSE_INCOME_BALANCE_AFTER_KEY: balance_after,
                WALLET_KEY: wallet
            }
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({INCOME_KEY: serializer.data}, status=HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        instance = Income.objects.get(id=kwargs.get(INCOME_ID_KEY))
        instance.delete()
        return Response({MESSAGE_KEY: 'Success'}, status=HTTP_204_NO_CONTENT)

    def list(self, request, *args, **kwargs):
        return Response(
            {EXPENSES_KEY: IncomeSerializer(Income.objects.filter(wallet=kwargs.get(INCOME_ID_KEY)), many=True).data}
        )
