from django.urls import path


from personal_wallet.utils_for_urls import LIST_VIEW_CONSTANT, CREATE_VIEW_CONSTANT, DETAIL_VIEW_CONSTANT,\
                                           UPDATE_VIEW_CONSTANT, DELETE_VIEW_CONSTANT
from .views import *    # TODO

# urlpatterns = [
#     path('{}/'.format(LIST_VIEW_CONSTANT), WalletListView.as_view()),
#     path('{}/'.format(CREATE_VIEW_CONSTANT), WalletCreateView.as_view()),
#     path('{}/'.format(DETAIL_VIEW_CONSTANT), WalletDetailView.as_view()),
#     path('{}/'.format(UPDATE_VIEW_CONSTANT), WalletUpdateView.as_view()),
#     path('{}/'.format(DELETE_VIEW_CONSTANT), )
# ]
