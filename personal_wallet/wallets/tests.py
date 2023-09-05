from datetime import date

from django.urls import reverse
from django.test import TestCase

from rest_framework import status

from personal_wallet.routes_util import routes_util
from wallets.models import Wallet
from users.models import WalletUser

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

WALLET_TEST_NAME = "TestWallet"
WALLET_TEST_NAME_INVALID = ""
WALLET_TEST_NAME_UPDATED = "TestWalletUpdated"
WALLET_TEST_INITIAL_BALANCE = 5000
WALLET_TEST_CURRENCY = 'USD'
RESPONSE_WALLET_KEY = 'wallet'

REQUEST_FORMAT = "json"
DATE_FORMAT = "%Y-%m-%d"


class WalletTests(TestCase):

    def setUp(self):
        self.wallets_create_url = reverse(routes_util.wallets_create_url_name())
        self.wallets_detail_url = reverse(routes_util.wallets_detail_url_name(), kwargs={"wallet_id": 1})
        self.wallets_detail_url_invalid = reverse(routes_util.wallets_detail_url_name(), kwargs={"wallet_id": 2})
        self.wallets_update_url = reverse(routes_util.wallets_update_url_name(), kwargs={"wallet_id": 1})
        self.wallets_delete_url = reverse(routes_util.wallets_delete_url_name(), kwargs={"wallet_id": 1})
        self.wallets_list_url = reverse(routes_util.wallets_list_url_name())
        self.registration_url = reverse(routes_util.users_registration_url_name())
        self.access_token = self.__perform_user_creation()
        self.auth_headers = {
            AUTHORIZATION_HEADERS_KEY: f"Bearer {self.access_token}"
        }
        self.response = self.__create_wallet()

    def __create_wallet(self):
        wallet_data = {
            WALLET_NAME_KEY: WALLET_TEST_NAME,
            WALLET_INITIAL_BALANCE_KEY: WALLET_TEST_INITIAL_BALANCE,
            WALLET_CURRENCY_KEY: WALLET_TEST_CURRENCY
        }
        return self.client.post(
            path=self.wallets_create_url,
            data=wallet_data,
            format=REQUEST_FORMAT,
            headers=self.auth_headers
        )

    def __perform_user_creation(self):
        user_data = {
            USER_USERNAME_KEY: TEST_USER_USERNAME,
            USER_PASSWORD_KEY: TEST_USER_PASSWORD
        }
        response = self.client.post(path=self.registration_url, data=user_data, format=REQUEST_FORMAT)
        return response.data[ACCESS_TOKEN_KEY]

    def test_wallet_create(self):

        # test response status of creation
        self.assertEqual(
            self.response.status_code, status.HTTP_201_CREATED
        )
        # test wallet name correspondence
        self.assertEqual(
            self.response.data[WALLET_NAME_KEY], WALLET_TEST_NAME
        )
        # test wallet initial balance correspondence
        self.assertEqual(
            float(self.response.data[WALLET_INITIAL_BALANCE_KEY]),
            float(WALLET_TEST_INITIAL_BALANCE)
        )
        # test wallet current balance witch = initial balance when wallet creating
        self.assertEqual(
            float(self.response.data[WALLET_CURRENT_BALANCE_KEY]),
            float(WALLET_TEST_INITIAL_BALANCE)
        )
        # test wallet date creation
        self.assertEqual(
            self.response.data[WALLET_DATE_CREATED_KEY],
            date.today().strftime(DATE_FORMAT)
        )
        # test that wallet is credit by default
        self.assertTrue(
            self.response.data[WALLET_IS_CREDIT_KEY]
        )
        # test created wallet referred to auth user
        self.assertEqual(
            self.response.data[WALLET_USER_KEY], 1
        )

    def test_wallet_create_invalid(self):
        wallet_data = {
            WALLET_NAME_KEY: WALLET_TEST_NAME_INVALID,
            WALLET_INITIAL_BALANCE_KEY: WALLET_TEST_INITIAL_BALANCE,
            WALLET_CURRENCY_KEY: WALLET_TEST_CURRENCY
        }
        response = self.client.post(
            path=self.wallets_create_url,
            data=wallet_data,
            format=REQUEST_FORMAT,
            headers=self.auth_headers
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_wallet_detail(self):
        response = self.client.get(
            path=self.wallets_detail_url,
            format=REQUEST_FORMAT,
            headers=self.auth_headers
        )
        # test getting needed wallet
        self.assertEqual(response.data[WALLET_ID_KEY], 1)
        # test wallet name correspondence
        self.assertEqual(
            response.data[WALLET_NAME_KEY], WALLET_TEST_NAME
        )
        # test wallet initial balance correspondence
        self.assertEqual(
            float(response.data[WALLET_INITIAL_BALANCE_KEY]),
            float(WALLET_TEST_INITIAL_BALANCE)
        )
        # test wallet current balance witch = initial balance when wallet creating
        self.assertEqual(
            float(response.data[WALLET_CURRENT_BALANCE_KEY]),
            float(WALLET_TEST_INITIAL_BALANCE)
        )
        # test wallet date creation
        self.assertEqual(
            response.data[WALLET_DATE_CREATED_KEY],
            date.today().strftime(DATE_FORMAT)
        )
        # test that wallet is credit by default
        self.assertTrue(
            response.data[WALLET_IS_CREDIT_KEY]
        )
        # test created wallet referred to auth user
        self.assertEqual(
            response.data[WALLET_USER_KEY], 1
        )

    def test_wallet_detail_invalid(self):
        response = self.client.get(
            path=self.wallets_detail_url_invalid,
            format=REQUEST_FORMAT,
            headers=self.auth_headers
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_wallet_update(self):
        update_data = {
            WALLET_NAME_KEY: WALLET_TEST_NAME_UPDATED
        }
        response = self.client.patch(
            path=self.wallets_update_url,
            data=update_data,
            format=REQUEST_FORMAT,
            content_type='application/json',
            headers=self.auth_headers
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[WALLET_NAME_KEY], WALLET_TEST_NAME_UPDATED)

    def test_wallet_update_invalid(self):
        update_data_invalid = {
            WALLET_NAME_KEY: WALLET_TEST_NAME_INVALID
        }
        response = self.client.patch(
            path=self.wallets_update_url,
            data=update_data_invalid,
            format=REQUEST_FORMAT,
            content_type='application/json',
            headers=self.auth_headers
        )
        wallet_instance = Wallet.objects.get(id=1)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(wallet_instance.name, WALLET_TEST_NAME)

    def test_wallet_destroy(self):
        response = self.client.delete(
            path=self.wallets_delete_url,
            format=REQUEST_FORMAT,
            headers=self.auth_headers
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_wallet_destroy_invalid(self):
        self.client.delete(
            path=self.wallets_delete_url,
            format=REQUEST_FORMAT,
            headers=self.auth_headers
        )
        # trying to delete wallet instance that has deleted
        response = self.client.delete(
            path=self.wallets_delete_url,
            format=REQUEST_FORMAT,
            headers=self.auth_headers
        )
        # test wallet delete after deleting this instance
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_wallet_list(self):
        response = self.client.get(
            path=self.wallets_list_url,
            format=REQUEST_FORMAT,
            headers=self.auth_headers
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
