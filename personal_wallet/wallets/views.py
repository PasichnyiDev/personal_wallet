from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Wallet


class WalletViewSet(viewsets.ModelViewSet):

    queryset = Wallet.objects.all()
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        pass

    def create(self, request, *args, **kwargs):
        pass

    def retrieve(self, request, *args, **kwargs):
        pass

    def partial_update(self, request, *args, **kwargs):
        pass

    def destroy(self, request, *args, **kwargs):
        pass