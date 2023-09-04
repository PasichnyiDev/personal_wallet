from django.urls import path

from personal_wallet.utils_for_urls import LIST_VIEW_CONSTANT, CREATE_VIEW_CONSTANT, DETAIL_VIEW_CONSTANT, \
    UPDATE_VIEW_CONSTANT, DELETE_VIEW_CONSTANT, WALLET_ID_CONSTANT, \
    EXPENSES_URL_KEY, EXPENSE_ID_CONSTANT, INCOMES_URL_KEY, INCOME_ID_CONSTANT
from personal_wallet.routes_util import routes_util
from .views import WalletViewSet, ExpenseViewSet, IncomeViewSet

urlpatterns = [
    # wallets urls
    path(
        route=routes_util.wallets_create_url(for_frontend=False),
        view=WalletViewSet.as_view({'post': 'create'}),
        name=routes_util.wallets_create_url_name()
    ),
    path(
        route=routes_util.wallets_detail_url(for_frontend=False),
        view=WalletViewSet.as_view({'get': 'retrieve'}),
        name=routes_util.wallets_detail_url_name()
    ),
    path(
        route=routes_util.wallets_update_url(for_frontend=False),
        view=WalletViewSet.as_view({'patch': 'partial_update'}),
        name=routes_util.wallets_update_url_name()
    ),
    path(
        route=routes_util.wallets_delete_url(for_frontend=False),
        view=WalletViewSet.as_view({'delete': 'destroy'}),
        name=routes_util.wallets_delete_url_name()
    ),
    path(
        route=routes_util.wallets_list_url(for_frontend=False),
        view=WalletViewSet.as_view({'get': 'list'}),
        name=routes_util.wallets_list_url_name()
    ),

    # expenses urls
    path(
        route=routes_util.expenses_create_url(for_frontend=False),
        view=ExpenseViewSet.as_view({'post': 'create'}),
        name=routes_util.expenses_create_url_name()
    ),
    path(
        route=routes_util.expenses_delete_url(for_frontend=False),
        view=ExpenseViewSet.as_view({'delete': 'destroy'}),
        name=routes_util.expenses_delete_url_name()
    ),
    path(
        route=routes_util.expenses_list_url(for_frontend=False),
        view=ExpenseViewSet.as_view({'get': 'list'}),
        name=routes_util.expenses_list_url_name()
    ),

    # incomes urls
    path(
        route=routes_util.incomes_create_url(for_frontend=False),
        view=IncomeViewSet.as_view({'post': 'create'}),
        name=routes_util.incomes_create_url_name()
    ),
    path(
        route=routes_util.incomes_delete_url(for_frontend=False),
        view=IncomeViewSet.as_view({'delete': 'destroy'}),
        name=routes_util.incomes_delete_url_name()
    ),
    path(
        route=routes_util.incomes_list_url(for_frontend=False),
        view=IncomeViewSet.as_view({'get': 'list'}),
        name=routes_util.incomes_list_url_name()
    ),
]
