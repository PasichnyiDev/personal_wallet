from django.urls import path

from personal_wallet.routes_util import routes_util
from .views import WalletViewSet, ExpenseViewSet, IncomeViewSet, \
                   get_currency_choices, get_expenses_choices, get_incomes_choices

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
    path(
        route=routes_util.currency_choices_url(for_frontend=False),
        view=get_currency_choices,
        name=routes_util.currency_choices_url_name()
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
    path(
        route=routes_util.expenses_choices_url(for_frontend=False),
        view=get_expenses_choices,
        name=routes_util.expenses_choices_url_name()
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
    path(
        route=routes_util.incomes_choices_url(for_frontend=False),
        view=get_incomes_choices,
        name=routes_util.incomes_choices_url_name()
    ),
]
