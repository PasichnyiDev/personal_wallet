import json

# base constants
ADMIN_URL_CONSTANT = 'admin/'
GET_URLS_CONSTANT = 'get_urls/'
LIST_VIEW_CONSTANT = 'list'
CREATE_VIEW_CONSTANT = 'create'
DETAIL_VIEW_CONSTANT = 'detail'
UPDATE_VIEW_CONSTANT = 'update'
DELETE_VIEW_CONSTANT = 'delete'
FIRST_ARG_CONSTANT = '{1}'
SECOND_ARG_CONSTANT = '{2}'
URLS_FILE_CONSTANT = 'urls'

# JWT
TOKEN_OBTAIN_URL_CONSTANT = 'token/'
TOKEN_REFRESH_URL_CONSTANT = 'token/refresh/'

# custom_user
CUSTOM_USER_URL_CONSTANT = 'users/'
CUSTOM_USER_APP_NAME = 'users'
CUSTOM_USER_PROFILE_URL_CONSTANT = 'profile/'
CUSTOM_USER_REGISTRATION_URL_CONSTANT = 'register/'

# wallet urls constants
WALLET_BASE_URL = 'v1/wallet/'
WALLET_ID_CONSTANT = '<int:wallet_id>'


def get_wallet_urls(for_frontend: bool = True):
    wallet_urls = {
        LIST_VIEW_CONSTANT: '{}{}/'.format(WALLET_BASE_URL, LIST_VIEW_CONSTANT),
        CREATE_VIEW_CONSTANT: '{}{}/'.format(WALLET_BASE_URL, CREATE_VIEW_CONSTANT),
        DETAIL_VIEW_CONSTANT: '{}{}/{}/'.format(
            WALLET_BASE_URL, DETAIL_VIEW_CONSTANT, FIRST_ARG_CONSTANT if for_frontend else WALLET_ID_CONSTANT),
        UPDATE_VIEW_CONSTANT: '{}{}/{}/'.format(
            WALLET_BASE_URL, UPDATE_VIEW_CONSTANT, FIRST_ARG_CONSTANT if for_frontend else WALLET_ID_CONSTANT),
        DELETE_VIEW_CONSTANT: '{}{}/{}/'.format(
            WALLET_BASE_URL, DELETE_VIEW_CONSTANT, FIRST_ARG_CONSTANT if for_frontend else WALLET_ID_CONSTANT)
    }
    return wallet_urls


# expense urls constants
def get_expense_base_url(for_frontend: bool = True):
    expense_base_url = '{}{}/expense/'.format(
        WALLET_BASE_URL, FIRST_ARG_CONSTANT if for_frontend else WALLET_ID_CONSTANT
    )
    return expense_base_url


EXPENSE_ID_CONSTANT = '<int:expense_id>'


def get_expense_urls(for_frontend: bool = True):
    expense_urls = {
        LIST_VIEW_CONSTANT: '{}{}/'.format(get_expense_base_url(for_frontend), LIST_VIEW_CONSTANT),
        CREATE_VIEW_CONSTANT: '{}{}/'.format(get_expense_base_url(for_frontend), CREATE_VIEW_CONSTANT),
        UPDATE_VIEW_CONSTANT: '{}{}/{}/'.format(
            get_expense_base_url(for_frontend),
            UPDATE_VIEW_CONSTANT,
            SECOND_ARG_CONSTANT if for_frontend else EXPENSE_ID_CONSTANT
        ),
        DELETE_VIEW_CONSTANT: '{}{}/{}/'.format(
            get_expense_base_url(for_frontend),
            DELETE_VIEW_CONSTANT,
            SECOND_ARG_CONSTANT if for_frontend else EXPENSE_ID_CONSTANT)
    }
    return expense_urls


# income urls constants
def get_income_base_url(for_frontend: bool = True):
    income_base_url = '{}{}/income/'.format(
        WALLET_BASE_URL, FIRST_ARG_CONSTANT if for_frontend else WALLET_ID_CONSTANT
    )
    return income_base_url


INCOME_ID_CONSTANT = '<int:income_id>'


def get_income_urls(for_frontend: bool = True):
    income_urls = {
        LIST_VIEW_CONSTANT: '{}{}/'.format(get_income_base_url(for_frontend), LIST_VIEW_CONSTANT),
        CREATE_VIEW_CONSTANT: '{}{}/'.format(get_income_base_url(for_frontend), CREATE_VIEW_CONSTANT),
        UPDATE_VIEW_CONSTANT: '{}{}/{}/'.format(
            get_income_base_url(for_frontend),
            UPDATE_VIEW_CONSTANT,
            SECOND_ARG_CONSTANT if for_frontend else INCOME_ID_CONSTANT
        ),
        DELETE_VIEW_CONSTANT: '{}{}/{}/'.format(
            get_income_base_url(for_frontend),
            DELETE_VIEW_CONSTANT,
            SECOND_ARG_CONSTANT if for_frontend else INCOME_ID_CONSTANT)
    }
    return income_urls


# urls for frontend
def get_urls(for_frontend: bool = True):
    urls_key = 'urls'
    wallet_key = 'wallet'
    expense_key = 'expense'
    income_key = 'income'

    data = {
        urls_key: {
            wallet_key: get_wallet_urls(for_frontend=for_frontend),
            expense_key: get_expense_urls(for_frontend=for_frontend),
            income_key: get_income_urls(for_frontend=for_frontend)
        }
    }
    return data


URLS_FOR_FRONTEND = get_urls(for_frontend=True)

if __name__ == '__main__':
    print(json.dumps(URLS_FOR_FRONTEND))
