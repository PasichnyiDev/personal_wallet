from django.urls import path

from personal_wallet.routes_util import routes_util

from .views import ExpensesByTypeListView, IncomesByTypeListView, TotalExpensesView, TotalIncomesView

urlpatterns = [
    path(
        route=routes_util.statistics_expenses_by_type_url(for_frontend=False),
        view=ExpensesByTypeListView.as_view(),
        name=routes_util.statistics_expenses_by_type_url_name()
    ),
    path(
        route=routes_util.statistics_incomes_by_type_url(for_frontend=False),
        view=IncomesByTypeListView.as_view(),
        name=routes_util.statistics_incomes_by_type_url_name()
    ),
    path(
        route=routes_util.statistics_expenses_total_url(for_frontend=False),
        view=TotalExpensesView.as_view(),
        name=routes_util.statistics_expenses_total_url_name()
    ),
    path(
        route=routes_util.statistics_incomes_total_url(for_frontend=False),
        view=TotalIncomesView.as_view(),
        name=routes_util.statistics_incomes_total_url_name()
    )
]
