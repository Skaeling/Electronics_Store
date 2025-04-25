from rest_framework import viewsets
from .models import NetworkNode
from .serializers import NetworkNodeSerializer, NetworkNodeUpdateSerializer


class SuppliersViewSet(viewsets.ModelViewSet):
    queryset = NetworkNode.objects.all()

    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return NetworkNodeUpdateSerializer
        return NetworkNodeSerializer

