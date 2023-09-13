from datetime import date

from django.urls import reverse
from django.test import TestCase

from rest_framework import status

from personal_wallet.routes_util import routes_util
from wallets.models import Wallet

USER_USERNAME_KEY = "username"
USER_PASSWORD_KEY = "password"

TEST_USER_USERNAME = "TestUserUsername"
TEST_USER_PASSWORD = "KVs45619572bhdn"

ACCESS_TOKEN_KEY = "access_token"
AUTHORIZATION_HEADERS_KEY = "Authorization"

WALLET_ID_KEY = "id"
WALLET_NAME_KEY = "name"
WALLET_INITIAL_BALANCE_KEY = "initial_balance"
WALLET_CURRENT_BALANCE_KEY = "current_balance"
WALLET_CURRENCY_KEY = "currency"
WALLET_DATE_CREATED_KEY = "date_created"
WALLET_IS_CREDIT_KEY = "is_credit_wallet"
WALLET_USER_KEY = "user"
WALLET_RESPONSE_KEY = 'wallet'

WALLET_TEST_NAME = "TestWallet"
WALLET_TEST_NAME_INVALID = ""
WALLET_TEST_NAME_UPDATED = "TestWalletUpdated"
WALLET_TEST_INITIAL_BALANCE = 5000
WALLET_TEST_INITIAL_BALANCE_INVALID = -5000
WALLET_TEST_CURRENCY = "USD"
WALLET_TEST_CURRENCY_INVALID = "jin"

EXPENSES_KEY = 'expenses'
EXPENSE_TEST_AMOUNT = 100
EXPENSE_TEST_AMOUNT_INVALID = -100
EXPENSE_TEST_TYPE = "FOOD"
EXPENSE_TEST_TYPE_INVALID = ""
EXPENSE_INCOME_AMOUNT_KEY = 'amount'
EXPENSE_INCOME_TYPE_KEY = 'type'
EXPENSE_INCOME_BALANCE_AFTER_KEY = 'balance_after'
EXPENSE_INCOME_DATE_CREATED_KEY = "date_created"

INCOMES_KEY = "incomes"
INCOME_TEST_AMOUNT = 100
INCOME_TEST_AMOUNT_INVALID = -100
INCOME_TEST_TYPE = 'SALES'
INCOME_TEST_TYPE_INVALID = ""

REQUEST_FORMAT = "json"
DATE_FORMAT = "%Y-%m-%d"
JS_FALSE = "false"
JS_TRUE = "true"


class UserCreationMixin(TestCase):
    def setUp(self) -> None:
        self._user_id = 1
        self._auth_headers = self.__build_auth_headers(token=self.__perform_user_creation())

    def __perform_user_creation(self):
        user_data = {USER_USERNAME_KEY: TEST_USER_USERNAME, USER_PASSWORD_KEY: TEST_USER_PASSWORD}
        response = self.client.post(
            path=reverse(routes_util.users_registration_url_name()),
            data=user_data,
            format=REQUEST_FORMAT
        )
        return response.data[ACCESS_TOKEN_KEY]

    @staticmethod
    def __build_auth_headers(token):
        return {
            AUTHORIZATION_HEADERS_KEY: f"Bearer {token}"
        }


class WalletCreationMixin(UserCreationMixin, TestCase):
    def setUp(self) -> None:
        super().setUp()
        self._wallet_id = 1

    def _create_wallet(self, is_credit=True):
        if is_credit:
            wallet_data = {
                WALLET_NAME_KEY: WALLET_TEST_NAME,
                WALLET_INITIAL_BALANCE_KEY: WALLET_TEST_INITIAL_BALANCE,
                WALLET_CURRENCY_KEY: WALLET_TEST_CURRENCY
            }
        else:
            wallet_data = {
                WALLET_NAME_KEY: WALLET_TEST_NAME,
                WALLET_INITIAL_BALANCE_KEY: WALLET_TEST_INITIAL_BALANCE,
                WALLET_CURRENCY_KEY: WALLET_TEST_CURRENCY,
                WALLET_IS_CREDIT_KEY: JS_FALSE
            }

        self.client.post(
            path=reverse(routes_util.wallets_create_url_name()),
            data=wallet_data,
            format=REQUEST_FORMAT,
            headers=self._auth_headers
        )


class WalletCreateTests(UserCreationMixin, TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.__wallet_create_url = reverse(routes_util.wallets_create_url_name())

    def test_wallet_create_valid(self):
        wallet_data = {
            WALLET_NAME_KEY: WALLET_TEST_NAME,
            WALLET_INITIAL_BALANCE_KEY: WALLET_TEST_INITIAL_BALANCE,
            WALLET_CURRENCY_KEY: WALLET_TEST_CURRENCY
        }
        response = self.client.post(
            path=self.__wallet_create_url,
            data=wallet_data,
            format=REQUEST_FORMAT,
            headers=self._auth_headers
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get(WALLET_NAME_KEY), WALLET_TEST_NAME)
        self.assertEqual(float(response.data.get(WALLET_INITIAL_BALANCE_KEY)),
                         round(float(WALLET_TEST_INITIAL_BALANCE), 2))
        self.assertEqual(float(response.data.get(WALLET_CURRENT_BALANCE_KEY)),
                         round(float(WALLET_TEST_INITIAL_BALANCE), 2))
        self.assertEqual(response.data.get(WALLET_CURRENCY_KEY), WALLET_TEST_CURRENCY)
        self.assertTrue(response.data.get(WALLET_IS_CREDIT_KEY))
        self.assertEqual(response.data.get(WALLET_DATE_CREATED_KEY), date.today().strftime(DATE_FORMAT))
        self.assertEqual(response.data.get(WALLET_USER_KEY), self._user_id)

    def test_wallet_create_invalid_wallet_name(self):
        wallet_data = {
            WALLET_NAME_KEY: WALLET_TEST_NAME_INVALID,
            WALLET_INITIAL_BALANCE_KEY: WALLET_TEST_INITIAL_BALANCE_INVALID,
            WALLET_CURRENCY_KEY: WALLET_TEST_CURRENCY
        }
        response = self.client.post(
            path=self.__wallet_create_url,
            data=wallet_data,
            format=REQUEST_FORMAT,
            headers=self._auth_headers
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_wallet_create_invalid_initial_balance(self):
        wallet_data = {
            WALLET_NAME_KEY: WALLET_TEST_NAME,
            WALLET_INITIAL_BALANCE_KEY: WALLET_TEST_INITIAL_BALANCE_INVALID,
            WALLET_CURRENCY_KEY: WALLET_TEST_CURRENCY
        }
        response = self.client.post(
            path=self.__wallet_create_url,
            data=wallet_data,
            format=REQUEST_FORMAT,
            headers=self._auth_headers
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_wallet_create_invalid_currency(self):
        wallet_data = {
            WALLET_NAME_KEY: WALLET_TEST_NAME,
            WALLET_INITIAL_BALANCE_KEY: WALLET_TEST_INITIAL_BALANCE,
            WALLET_CURRENCY_KEY: WALLET_TEST_CURRENCY_INVALID
        }
        response = self.client.post(
            path=self.__wallet_create_url,
            data=wallet_data,
            format=REQUEST_FORMAT,
            headers=self._auth_headers
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class WalletDetailTests(WalletCreationMixin, TestCase):

    def setUp(self) -> None:
        super().setUp()
        self._create_wallet()
        self.__wallet_detail_url = reverse(routes_util.wallets_detail_url_name(), kwargs={"wallet_id": self._wallet_id})
        self.__wallet_detail_url_invalid = reverse(
            routes_util.wallets_detail_url_name(), kwargs={"wallet_id": 2}
        )

    def test_wallet_detail(self):
        response = self.client.get(
            path=self.__wallet_detail_url,
            format=REQUEST_FORMAT,
            headers=self._auth_headers
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get(WALLET_NAME_KEY), WALLET_TEST_NAME)
        self.assertEqual(float(response.data.get(WALLET_INITIAL_BALANCE_KEY)),
                         round(float(WALLET_TEST_INITIAL_BALANCE), 2))
        self.assertEqual(float(response.data.get(WALLET_CURRENT_BALANCE_KEY)),
                         round(float(WALLET_TEST_INITIAL_BALANCE), 2))
        self.assertEqual(response.data.get(WALLET_CURRENCY_KEY), WALLET_TEST_CURRENCY)
        self.assertTrue(response.data.get(WALLET_IS_CREDIT_KEY))
        self.assertEqual(response.data.get(WALLET_DATE_CREATED_KEY), date.today().strftime(DATE_FORMAT))
        self.assertEqual(response.data.get(WALLET_USER_KEY), self._user_id)

    def test_wallet_detail_invalid(self):
        response = self.client.get(
            path=self.__wallet_detail_url_invalid,
            format=REQUEST_FORMAT,
            headers=self._auth_headers
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class WalletUpdateTests(WalletCreationMixin, TestCase):

    def setUp(self) -> None:
        super(WalletUpdateTests, self).setUp()
        self._create_wallet()
        self.__wallet_update_url = reverse(routes_util.wallets_update_url_name(), kwargs={"wallet_id": self._wallet_id})

    def test_wallet_update_wallet_name(self):
        updated_wallet_data = {
            WALLET_NAME_KEY: WALLET_TEST_NAME_UPDATED
        }
        response = self.client.patch(
            path=self.__wallet_update_url,
            data=updated_wallet_data,
            format=REQUEST_FORMAT,
            headers=self._auth_headers,
            content_type='application/json'
        )
        wallet = Wallet.objects.get(id=self._wallet_id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get(WALLET_NAME_KEY), wallet.name)

    def test_wallet_update_wallet_name_invalid(self):
        updated_wallet_data = {
            WALLET_NAME_KEY: WALLET_TEST_NAME_INVALID
        }
        response = self.client.patch(
            path=self.__wallet_update_url,
            data=updated_wallet_data,
            format=REQUEST_FORMAT,
            headers=self._auth_headers,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_wallet_update_wallet_currency(self):
        updated_wallet_data = {
            WALLET_CURRENCY_KEY: WALLET_TEST_CURRENCY
        }
        response = self.client.patch(
            path=self.__wallet_update_url,
            data=updated_wallet_data,
            format=REQUEST_FORMAT,
            headers=self._auth_headers,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_wallet_update_wallet_initial_balance(self):
        updated_wallet_data = {
            WALLET_INITIAL_BALANCE_KEY: WALLET_TEST_INITIAL_BALANCE
        }
        response = self.client.patch(
            path=self.__wallet_update_url,
            data=updated_wallet_data,
            format=REQUEST_FORMAT,
            headers=self._auth_headers,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_wallet_update_wallet_current_balance(self):
        updated_wallet_data = {
            WALLET_CURRENT_BALANCE_KEY: WALLET_TEST_INITIAL_BALANCE
        }
        response = self.client.patch(
            path=self.__wallet_update_url,
            data=updated_wallet_data,
            format=REQUEST_FORMAT,
            headers=self._auth_headers,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_wallet_update_wallet_is_credit(self):
        updated_wallet_data = {
            WALLET_IS_CREDIT_KEY: JS_FALSE
        }
        response = self.client.patch(
            path=self.__wallet_update_url,
            data=updated_wallet_data,
            format=REQUEST_FORMAT,
            headers=self._auth_headers,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_wallet_update_wallet_date_created(self):
        updated_wallet_data = {
            WALLET_DATE_CREATED_KEY: date.today().strftime(DATE_FORMAT)
        }
        response = self.client.patch(
            path=self.__wallet_update_url,
            data=updated_wallet_data,
            format=REQUEST_FORMAT,
            headers=self._auth_headers,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_wallet_update_wallet_user(self):
        updated_wallet_data = {
            WALLET_USER_KEY: 2
        }
        response = self.client.patch(
            path=self.__wallet_update_url,
            data=updated_wallet_data,
            format=REQUEST_FORMAT,
            headers=self._auth_headers,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class WalletDeleteTests(WalletCreationMixin, TestCase):

    def setUp(self) -> None:
        super(WalletDeleteTests, self).setUp()
        self._create_wallet()
        self.__wallet_delete_url = reverse(routes_util.wallets_delete_url_name(), kwargs={"wallet_id": self._wallet_id})
        self.__wallet_delete_url_invalid = reverse(routes_util.wallets_delete_url_name(), kwargs={"wallet_id": 2})

    def test_wallet_delete(self):
        response = self.client.delete(
            path=self.__wallet_delete_url,
            format=REQUEST_FORMAT,
            headers=self._auth_headers
        )
        wallets = Wallet.objects.all()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(wallets), 0)

    def test_wallet_delete_invalid(self):
        response = self.client.delete(
            path=self.__wallet_delete_url_invalid,
            format=REQUEST_FORMAT,
            headers=self._auth_headers
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class WalletListTests(WalletCreationMixin, TestCase):

    def setUp(self) -> None:
        super(WalletListTests, self).setUp()
        self._create_wallet()
        self.__wallet_list_url = reverse(routes_util.wallets_list_url_name())

    def test_wallet_list(self):
        response = self.client.get(
            path=self.__wallet_list_url,
            format=REQUEST_FORMAT,
            headers=self._auth_headers
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class ExpenseCreationMixin(UserCreationMixin, TestCase):
    def _create_expense(self, amount=EXPENSE_TEST_AMOUNT):
        expense_data = {
            EXPENSE_INCOME_AMOUNT_KEY: amount,
            EXPENSE_INCOME_TYPE_KEY: EXPENSE_TEST_TYPE
        }
        return self.client.post(
            path=reverse(routes_util.expenses_create_url_name(), kwargs={"wallet_id": 1}),
            data=expense_data,
            format=REQUEST_FORMAT,
            headers=self._auth_headers
        )


class ExpenseCreateTests(WalletCreationMixin, TestCase):

    def setUp(self) -> None:
        super(ExpenseCreateTests, self).setUp()
        self._create_wallet()
        self.__expense_create_url = reverse(routes_util.expenses_create_url_name(),
                                            kwargs={"wallet_id": self._wallet_id})

    def test_expense_create(self):
        expense_data = {
            EXPENSE_INCOME_AMOUNT_KEY: EXPENSE_TEST_AMOUNT,
            EXPENSE_INCOME_TYPE_KEY: EXPENSE_TEST_TYPE
        }
        response = self.client.post(
            path=self.__expense_create_url,
            data=expense_data,
            format=REQUEST_FORMAT,
            headers=self._auth_headers
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(float(response.data.get(EXPENSE_INCOME_AMOUNT_KEY)), round(float(EXPENSE_TEST_AMOUNT), 2))
        self.assertEqual(response.data.get(EXPENSE_INCOME_TYPE_KEY), EXPENSE_TEST_TYPE)
        self.assertEqual(response.data.get(EXPENSE_INCOME_DATE_CREATED_KEY), date.today().strftime(DATE_FORMAT))
        self.assertEqual(float(response.data.get(EXPENSE_INCOME_BALANCE_AFTER_KEY)),
                         round(float(WALLET_TEST_INITIAL_BALANCE-EXPENSE_TEST_AMOUNT), 2))
        self.assertEqual(response.data.get(WALLET_RESPONSE_KEY), self._wallet_id)

    def test_expense_create_amount_invalid(self):
        expense_data = {
            EXPENSE_INCOME_AMOUNT_KEY: EXPENSE_TEST_AMOUNT_INVALID,
            EXPENSE_INCOME_TYPE_KEY: EXPENSE_TEST_TYPE
        }
        response = self.client.post(
            path=self.__expense_create_url,
            data=expense_data,
            format=REQUEST_FORMAT,
            headers=self._auth_headers
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_expense_create_type_invalid(self):
        expense_data = {
            EXPENSE_INCOME_AMOUNT_KEY: EXPENSE_TEST_AMOUNT,
            EXPENSE_INCOME_TYPE_KEY: EXPENSE_TEST_TYPE_INVALID
        }
        response = self.client.post(
            path=self.__expense_create_url,
            data=expense_data,
            format=REQUEST_FORMAT,
            headers=self._auth_headers
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ExpenseDeleteTests(ExpenseCreationMixin, WalletCreationMixin, TestCase):

    def setUp(self) -> None:
        super(ExpenseDeleteTests, self).setUp()
        self._create_wallet()
        self._create_expense()
        self.__expense_delete_url = reverse(routes_util.expenses_delete_url_name(),
                                            kwargs={"wallet_id": self._wallet_id, "expense_id": 1})
        self.__expense_delete_url_invalid = reverse(routes_util.expenses_delete_url_name(),
                                            kwargs={"wallet_id": self._wallet_id, "expense_id": 2})

    def test_expense_delete(self):
        response = self.client.delete(
            path=self.__expense_delete_url,
            format=REQUEST_FORMAT,
            headers=self._auth_headers
        )
        wallet = Wallet.objects.get(id=self._wallet_id)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(round(float(wallet.current_balance), 2),
                         round(float(WALLET_TEST_INITIAL_BALANCE), 2))

    def test_expense_delete_invalid_expense_id(self):
        response = self.client.delete(
            path=self.__expense_delete_url_invalid,
            format=REQUEST_FORMAT,
            headers=self._auth_headers
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class ExpenseListTests(ExpenseCreationMixin, WalletCreationMixin, TestCase):

    def setUp(self) -> None:
        super(ExpenseListTests, self).setUp()
        self._create_wallet()
        self._create_expense()
        self.__expenses_list_url = reverse(routes_util.expenses_list_url_name(), kwargs={"wallet_id": self._wallet_id})

    def test_expenses_list(self):
        response = self.client.get(
            path=self.__expenses_list_url,
            format=REQUEST_FORMAT,
            headers=self._auth_headers
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get(EXPENSES_KEY)), 1)


class IncomeCreationMixin(WalletCreationMixin, TestCase):

    def _create_income(self, amount=INCOME_TEST_AMOUNT):
        income_data = {
            EXPENSE_INCOME_AMOUNT_KEY: amount,
            EXPENSE_INCOME_TYPE_KEY: INCOME_TEST_TYPE
        }
        return self.client.post(
            path=reverse(routes_util.incomes_create_url_name(), kwargs={"wallet_id": 1}),
            data=income_data,
            format=REQUEST_FORMAT,
            headers=self._auth_headers
        )


class IncomeCreateTests(WalletCreationMixin, TestCase):

    def setUp(self) -> None:
        super(IncomeCreateTests, self).setUp()
        self._create_wallet()
        self.__income_create_url = reverse(routes_util.incomes_create_url_name(), kwargs={"wallet_id": self._wallet_id})

    def test_income_create(self):
        income_data = {
            EXPENSE_INCOME_AMOUNT_KEY: INCOME_TEST_AMOUNT,
            EXPENSE_INCOME_TYPE_KEY: INCOME_TEST_TYPE
        }
        response = self.client.post(
            path=self.__income_create_url,
            data=income_data,
            format=REQUEST_FORMAT,
            headers=self._auth_headers
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(float(response.data.get(EXPENSE_INCOME_AMOUNT_KEY)), round(float(INCOME_TEST_AMOUNT), 2))
        self.assertEqual(response.data.get(EXPENSE_INCOME_TYPE_KEY), INCOME_TEST_TYPE)
        self.assertEqual(response.data.get(EXPENSE_INCOME_DATE_CREATED_KEY), date.today().strftime(DATE_FORMAT))
        self.assertEqual(float(response.data.get(EXPENSE_INCOME_BALANCE_AFTER_KEY)),
                         round(float(WALLET_TEST_INITIAL_BALANCE+INCOME_TEST_AMOUNT), 2))
        self.assertEqual(response.data.get(WALLET_RESPONSE_KEY), self._wallet_id)

    def test_income_create_invalid_amount(self):
        income_data = {
            EXPENSE_INCOME_AMOUNT_KEY: INCOME_TEST_AMOUNT_INVALID,
            EXPENSE_INCOME_TYPE_KEY: INCOME_TEST_TYPE
        }
        response = self.client.post(
            path=self.__income_create_url,
            data=income_data,
            format=REQUEST_FORMAT,
            headers=self._auth_headers
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_income_create_invalid_type(self):
        income_data = {
            EXPENSE_INCOME_AMOUNT_KEY: INCOME_TEST_AMOUNT,
            EXPENSE_INCOME_TYPE_KEY: INCOME_TEST_TYPE_INVALID
        }
        response = self.client.post(
            path=self.__income_create_url,
            data=income_data,
            format=REQUEST_FORMAT,
            headers=self._auth_headers
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class IncomeDeleteTests(IncomeCreationMixin, WalletCreationMixin, TestCase):

    def setUp(self) -> None:
        super(IncomeDeleteTests, self).setUp()
        self._create_wallet()
        self._create_income()
        self.__income_delete_url = reverse(routes_util.incomes_delete_url_name(),
                                           kwargs={"wallet_id": self._wallet_id, "income_id": 1})
        self.__income_delete_url_invalid = reverse(routes_util.incomes_delete_url_name(),
                                           kwargs={"wallet_id": self._wallet_id, "income_id": 2})

    def test_income_delete(self):
        response = self.client.delete(
            path=self.__income_delete_url,
            format=REQUEST_FORMAT,
            headers=self._auth_headers
        )
        wallet = Wallet.objects.get(id=self._wallet_id)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(round(float(wallet.current_balance), 2),
                         round(float(WALLET_TEST_INITIAL_BALANCE), 2))

    def test_income_delete_invalid_expense_id(self):
        response = self.client.delete(
            path=self.__income_delete_url_invalid,
            format=REQUEST_FORMAT,
            headers=self._auth_headers
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class IncomeListTests(IncomeCreationMixin, WalletCreationMixin, TestCase):
    def setUp(self) -> None:
        super(IncomeListTests, self).setUp()
        self._create_wallet()
        self._create_income()
        self.__incomes_list_url = reverse(routes_util.incomes_list_url_name(), kwargs={"wallet_id": self._wallet_id})

    def test_expenses_list(self):
        response = self.client.get(
            path=self.__incomes_list_url,
            format=REQUEST_FORMAT,
            headers=self._auth_headers
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get(INCOMES_KEY)), 1)


class ExpenseIncomeComplexDeleteTests(IncomeCreationMixin, ExpenseCreationMixin, WalletCreationMixin, TestCase):

    def setUp(self) -> None:
        super(ExpenseIncomeComplexDeleteTests, self).setUp()
        self._create_wallet(is_credit=False)
        self.__income_delete_url = reverse(routes_util.incomes_delete_url_name(),
                                           kwargs={"wallet_id": self._wallet_id, "income_id": 1})

    def test_delete_income_impossibility(self):
        self._create_income()                   # current balance 5000 + 100 = 5100
        self._create_expense(amount=5050)       # current balance 5100 - 5050 = 50

        # trying to delete income which thinks to be impossible in not credit wallet because of 50 - 100 < 0
        response = self.client.delete(
            path=self.__income_delete_url,
            format=REQUEST_FORMAT,
            headers=self._auth_headers
        )
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)


class ChoicesTests(TestCase):

    def setUp(self) -> None:
        self.__currency_choices_url = reverse(routes_util.currency_choices_url_name())
        self.__expenses_choices_url = reverse(routes_util.expenses_choices_url_name())
        self.__incomes_choices_url = reverse(routes_util.incomes_choices_url_name())

    def test_currency_choices(self):
        response = self.client.get(
            path=self.__currency_choices_url,
            format=REQUEST_FORMAT
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_expenses_choices(self):
        response = self.client.get(
            path=self.__expenses_choices_url,
            format=REQUEST_FORMAT
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_incomes_choices(self):
        response = self.client.get(
            path=self.__incomes_choices_url,
            format=REQUEST_FORMAT
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

