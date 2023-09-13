from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from rest_framework import status

from personal_wallet.routes_util import routes_util
from wallets.models import Expense, Wallet, Income

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
EXPENSE_TEST_AMOUNT = 100.25
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

PERIOD_PARAM_KEY = "period"
PERIOD_WEEK = "week"
PERIOD_MONTH = "month"
PERIOD_QUARTER = "quarter"
PERIOD_YEAR = "year"


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


class ExpensesByTypeTests(WalletCreationMixin, TestCase):

    def setUp(self) -> None:
        super().setUp()
        self._create_wallet()

    def statistics_expenses_by_type_url(self, expense_type: str):
        return reverse(routes_util.statistics_expenses_by_type_url_name(),
                       kwargs={"wallet_id": self._wallet_id, "type": expense_type})

    def __create_expense(self, amount: int = EXPENSE_TEST_AMOUNT, expense_type: str = EXPENSE_TEST_TYPE):
        expense_data = {
            EXPENSE_INCOME_AMOUNT_KEY: amount,
            EXPENSE_INCOME_TYPE_KEY: expense_type
        }
        return self.client.post(
            path=reverse(routes_util.expenses_create_url_name(), kwargs={"wallet_id": self._wallet_id}),
            data=expense_data,
            format=REQUEST_FORMAT,
            headers=self._auth_headers
        )

    def test_statistics_expenses_by_type(self):
        # creating three food expenses
        food_expense_type = "FOOD"
        food_expense_count = 3
        for i in range(food_expense_count):
            self.__create_expense(expense_type=food_expense_type)

        # creating three loan expenses
        loan_expense_type = "LOAN"
        loan_expense_count = 2
        for k in range(loan_expense_count):
            self.__create_expense(expense_type=loan_expense_type)

        response = self.client.get(
            path=self.statistics_expenses_by_type_url(expense_type=food_expense_type),
            format=REQUEST_FORMAT,
            headers=self._auth_headers
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), food_expense_count)

        response = self.client.get(
            path=self.statistics_expenses_by_type_url(expense_type=loan_expense_type),
            format=REQUEST_FORMAT,
            headers=self._auth_headers
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), loan_expense_count)


class ExpensesByTypeWithPeriodTests(WalletCreationMixin, TestCase):
    def setUp(self) -> None:
        super().setUp()
        self._create_wallet()

    def __create_expense_with_custom_date(
            self,
            date: tuple,
            amount: int = EXPENSE_TEST_AMOUNT,
            expense_type: str = EXPENSE_TEST_TYPE,
    ):
        custom_date = timezone.datetime(*date).date()
        wallet = Wallet.objects.get(id=self._wallet_id)
        balance_after = float(wallet.current_balance) - float(amount)
        wallet.current_balance = balance_after
        wallet.save()

        return Expense.objects.create(
            amount=amount,
            type=expense_type,
            balance_after=balance_after,
            date_created=custom_date,
            wallet=wallet
        )

    def statistics_expenses_by_type_url(self, expense_type: str):
        return reverse(routes_util.statistics_expenses_by_type_url_name(),
                       kwargs={"wallet_id": self._wallet_id, "type": expense_type})

    def test_statistics_expenses_by_type_with_period(self):
        now = timezone.now()
        dates = [
            # periods in week
            (now.year, now.month, (now - timezone.timedelta(days=3)).day),
            (now.year, now.month, (now - timezone.timedelta(days=3)).day),
            (now.year, now.month, (now - timezone.timedelta(days=3)).day),
            # periods not in week
            (now.year, now.month, (now - timezone.timedelta(days=10)).day),
            (now.year, now.month, (now - timezone.timedelta(days=10)).day),
            (now.year, now.month, (now - timezone.timedelta(days=10)).day)
        ]
        for date in dates:
            self.__create_expense_with_custom_date(date=date)

        query_params = {PERIOD_PARAM_KEY: PERIOD_WEEK}
        response = self.client.get(
            path=self.statistics_expenses_by_type_url(expense_type=EXPENSE_TEST_TYPE),
            data=query_params,
            format=REQUEST_FORMAT,
            headers=self._auth_headers
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)


class ExpensesTotalTests(WalletCreationMixin, TestCase):

    def setUp(self) -> None:
        super().setUp()
        self._create_wallet()
        self.__statistics_expenses_total_url = reverse(routes_util.statistics_expenses_total_url_name(),
                                                       kwargs={"wallet_id": self._wallet_id})

    def __create_expense_with_custom_date(
            self,
            date: tuple,
            amount: int = EXPENSE_TEST_AMOUNT,
            expense_type: str = EXPENSE_TEST_TYPE,
    ):
        custom_date = timezone.datetime(*date).date()
        wallet = Wallet.objects.get(id=self._wallet_id)
        balance_after = float(wallet.current_balance) - float(amount)
        wallet.current_balance = balance_after
        wallet.save()

        return Expense.objects.create(
            amount=amount,
            type=expense_type,
            balance_after=balance_after,
            date_created=custom_date,
            wallet=wallet
        )

    @staticmethod
    def __create_all_dates(
            week_count: int = 3,
            month_count: int = 3,
            quarter_count: int = 3,
            year_count: int = 3
    ):
        now = timezone.now()
        dates = []
        for _ in range(week_count):
            dates.append(
                (
                    (now - timezone.timedelta(days=3)).year,
                    (now - timezone.timedelta(days=3)).month,
                    (now - timezone.timedelta(days=3)).day
                )
            )
        for _ in range(month_count):
            dates.append(
                (
                    (now - timezone.timedelta(days=10)).year,
                    (now - timezone.timedelta(days=10)).month,
                    (now - timezone.timedelta(days=10)).day
                )
            )
        for _ in range(quarter_count):
            dates.append(
                (
                    (now - timezone.timedelta(days=40)).year,
                    (now - timezone.timedelta(days=40)).month,
                    (now - timezone.timedelta(days=40)).day
                )
            )
        for _ in range(year_count):
            dates.append(
                (
                    (now - timezone.timedelta(days=130)).year,
                    (now - timezone.timedelta(days=130)).month,
                    (now - timezone.timedelta(days=130)).day
                )
            )
        return dates

    def test_expenses_total_week(self):
        week_expenses_count = 5
        week_total_amount_test = EXPENSE_TEST_AMOUNT * week_expenses_count
        dates = self.__create_all_dates(week_count=week_expenses_count)
        for date in dates:
            self.__create_expense_with_custom_date(date=date)

        query_params = {PERIOD_PARAM_KEY: PERIOD_WEEK}
        response = self.client.get(
            path=self.__statistics_expenses_total_url,
            data=query_params,
            format=REQUEST_FORMAT,
            headers=self._auth_headers
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(float(response.data['total']), float(week_total_amount_test))

    def test_expenses_total_month(self):
        month_expenses_count = 5
        month_total_amount_test = EXPENSE_TEST_AMOUNT * (month_expenses_count + 3)  # 3 in week by default
        dates = self.__create_all_dates(month_count=month_expenses_count)
        for date in dates:
            self.__create_expense_with_custom_date(date=date)

        query_params = {PERIOD_PARAM_KEY: PERIOD_MONTH}
        response = self.client.get(
            path=self.__statistics_expenses_total_url,
            data=query_params,
            format=REQUEST_FORMAT,
            headers=self._auth_headers
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(float(response.data['total']), float(month_total_amount_test))

    def test_expenses_total_quarter(self):
        quarter_expenses_count = 5

        # 3 in week and month by default
        quarter_total_amount_test = EXPENSE_TEST_AMOUNT * (quarter_expenses_count + 3 + 3)
        dates = self.__create_all_dates(quarter_count=quarter_expenses_count)
        for date in dates:
            self.__create_expense_with_custom_date(date=date)

        query_params = {PERIOD_PARAM_KEY: PERIOD_QUARTER}
        response = self.client.get(
            path=self.__statistics_expenses_total_url,
            data=query_params,
            format=REQUEST_FORMAT,
            headers=self._auth_headers
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(float(response.data['total']), float(quarter_total_amount_test))

    def test_expenses_total_year(self):
        year_expenses_count = 5

        # 3 in week and month and quarter by default
        year_total_amount_test = EXPENSE_TEST_AMOUNT * (year_expenses_count + 3 + 3 + 3)
        dates = self.__create_all_dates(year_count=year_expenses_count)
        for date in dates:
            self.__create_expense_with_custom_date(date=date)

        query_params = {PERIOD_PARAM_KEY: PERIOD_YEAR}
        response = self.client.get(
            path=self.__statistics_expenses_total_url,
            data=query_params,
            format=REQUEST_FORMAT,
            headers=self._auth_headers
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(float(response.data['total']), float(year_total_amount_test))


class IncomesByTypeTests(WalletCreationMixin, TestCase):
    def setUp(self) -> None:
        super().setUp()
        self._create_wallet()

    def statistics_incomes_by_type_url(self, income_type: str):
        return reverse(routes_util.statistics_incomes_by_type_url_name(),
                       kwargs={"wallet_id": self._wallet_id, "type": income_type})

    def __create_income(self, amount: int = INCOME_TEST_AMOUNT, income_type: str = INCOME_TEST_TYPE):
        wallet = Wallet.objects.get(id=self._wallet_id)
        balance_after = float(wallet.current_balance) + float(amount)
        wallet.current_balance = balance_after
        wallet.save()
        return Income.objects.create(
            amount=amount,
            type=income_type,
            balance_after=balance_after,
            date_created=timezone.now().date(),
            wallet=wallet
        )

    def test_statistics_expenses_by_type(self):
        # creating three PENSION incomes
        pension_income_type = "PENSION"
        pension_income_count = 3
        for i in range(pension_income_count):
            self.__create_income(income_type=pension_income_type)

        # creating three GRANT incomes
        grant_income_type = "GRANT"
        grant_income_count = 2
        for k in range(grant_income_count):
            self.__create_income(income_type=grant_income_type)

        response = self.client.get(
            path=self.statistics_incomes_by_type_url(income_type=pension_income_type),
            format=REQUEST_FORMAT,
            headers=self._auth_headers
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), pension_income_count)

        response = self.client.get(
            path=self.statistics_incomes_by_type_url(income_type=grant_income_type),
            format=REQUEST_FORMAT,
            headers=self._auth_headers
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), grant_income_count)


class IncomesByTypeWithPeriodTests(WalletCreationMixin, TestCase):
    def setUp(self) -> None:
        super().setUp()
        self._create_wallet()

    def __create_income_with_custom_date(
            self,
            date: tuple,
            amount: int = INCOME_TEST_AMOUNT,
            income_type: str = INCOME_TEST_TYPE,
    ):
        custom_date = timezone.datetime(*date).date()
        wallet = Wallet.objects.get(id=self._wallet_id)
        balance_after = float(wallet.current_balance) + float(amount)
        wallet.current_balance = balance_after
        wallet.save()

        return Income.objects.create(
            amount=amount,
            type=income_type,
            balance_after=balance_after,
            date_created=custom_date,
            wallet=wallet
        )

    def statistics_incomes_by_type_url(self, income_type: str):
        return reverse(routes_util.statistics_incomes_by_type_url_name(),
                       kwargs={"wallet_id": self._wallet_id, "type": income_type})

    def test_statistics_expenses_by_type_with_period(self):
        now = timezone.now()
        dates = [
            # periods in week
            (now.year, now.month, (now - timezone.timedelta(days=3)).day),
            (now.year, now.month, (now - timezone.timedelta(days=3)).day),
            (now.year, now.month, (now - timezone.timedelta(days=3)).day),
            # periods not in week
            (now.year, now.month, (now - timezone.timedelta(days=10)).day),
            (now.year, now.month, (now - timezone.timedelta(days=10)).day),
            (now.year, now.month, (now - timezone.timedelta(days=10)).day)
        ]
        for date in dates:
            self.__create_income_with_custom_date(date=date)

        query_params = {PERIOD_PARAM_KEY: PERIOD_WEEK}
        response = self.client.get(
            path=self.statistics_incomes_by_type_url(income_type=INCOME_TEST_TYPE),
            data=query_params,
            format=REQUEST_FORMAT,
            headers=self._auth_headers
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)


class IncomesTotalTests(WalletCreationMixin, TestCase):

    def setUp(self) -> None:
        super().setUp()
        self._create_wallet()
        self.__statistics_incomes_total_url = reverse(routes_util.statistics_incomes_total_url_name(),
                                                      kwargs={"wallet_id": self._wallet_id})

    def __create_income_with_custom_date(
            self,
            date: tuple,
            amount: int = INCOME_TEST_AMOUNT,
            income_type: str = INCOME_TEST_TYPE,
    ):
        custom_date = timezone.datetime(*date).date()
        wallet = Wallet.objects.get(id=self._wallet_id)
        balance_after = float(wallet.current_balance) + float(amount)
        wallet.current_balance = balance_after
        wallet.save()

        return Income.objects.create(
            amount=amount,
            type=income_type,
            balance_after=balance_after,
            date_created=custom_date,
            wallet=wallet
        )

    @staticmethod
    def __create_all_dates(
            week_count: int = 3,
            month_count: int = 3,
            quarter_count: int = 3,
            year_count: int = 3
    ):
        now = timezone.now()
        dates = []
        for _ in range(week_count):
            dates.append(
                (
                    (now - timezone.timedelta(days=3)).year,
                    (now - timezone.timedelta(days=3)).month,
                    (now - timezone.timedelta(days=3)).day
                )
            )
        for _ in range(month_count):
            dates.append(
                (
                    (now - timezone.timedelta(days=10)).year,
                    (now - timezone.timedelta(days=10)).month,
                    (now - timezone.timedelta(days=10)).day
                )
            )
        for _ in range(quarter_count):
            dates.append(
                (
                    (now - timezone.timedelta(days=40)).year,
                    (now - timezone.timedelta(days=40)).month,
                    (now - timezone.timedelta(days=40)).day
                )
            )
        for _ in range(year_count):
            dates.append(
                (
                    (now - timezone.timedelta(days=130)).year,
                    (now - timezone.timedelta(days=130)).month,
                    (now - timezone.timedelta(days=130)).day
                )
            )
        return dates

    def test_incomes_total_week(self):
        week_incomes_count = 5
        week_total_amount_test = INCOME_TEST_AMOUNT * week_incomes_count
        dates = self.__create_all_dates(week_count=week_incomes_count)
        for date in dates:
            self.__create_income_with_custom_date(date=date)

        query_params = {PERIOD_PARAM_KEY: PERIOD_WEEK}
        response = self.client.get(
            path=self.__statistics_incomes_total_url,
            data=query_params,
            format=REQUEST_FORMAT,
            headers=self._auth_headers
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(float(response.data['total']), float(week_total_amount_test))

    def test_incomes_total_month(self):
        month_incomes_count = 5
        month_total_amount_test = INCOME_TEST_AMOUNT * (month_incomes_count + 3)  # 3 in week by default
        dates = self.__create_all_dates(month_count=month_incomes_count)
        for date in dates:
            self.__create_income_with_custom_date(date=date)

        query_params = {PERIOD_PARAM_KEY: PERIOD_MONTH}
        response = self.client.get(
            path=self.__statistics_incomes_total_url,
            data=query_params,
            format=REQUEST_FORMAT,
            headers=self._auth_headers
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(float(response.data['total']), float(month_total_amount_test))

    def test_incomes_total_quarter(self):
        quarter_incomes_count = 5

        # 3 in week and month by default
        quarter_total_amount_test = INCOME_TEST_AMOUNT * (quarter_incomes_count + 3 + 3)
        dates = self.__create_all_dates(quarter_count=quarter_incomes_count)
        for date in dates:
            self.__create_income_with_custom_date(date=date)

        query_params = {PERIOD_PARAM_KEY: PERIOD_QUARTER}
        response = self.client.get(
            path=self.__statistics_incomes_total_url,
            data=query_params,
            format=REQUEST_FORMAT,
            headers=self._auth_headers
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(float(response.data['total']), float(quarter_total_amount_test))

    def test_incomes_total_year(self):
        year_incomes_count = 5

        # 3 in week and month and quarter by default
        year_total_amount_test = INCOME_TEST_AMOUNT * (year_incomes_count + 3 + 3 + 3)
        dates = self.__create_all_dates(year_count=year_incomes_count)
        for date in dates:
            self.__create_income_with_custom_date(date=date)

        query_params = {PERIOD_PARAM_KEY: PERIOD_YEAR}
        response = self.client.get(
            path=self.__statistics_incomes_total_url,
            data=query_params,
            format=REQUEST_FORMAT,
            headers=self._auth_headers
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(float(response.data['total']), float(year_total_amount_test))
