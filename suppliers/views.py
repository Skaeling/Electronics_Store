from rest_framework import viewsets
from .models import NetworkNode
from .serializers import NetworkNodeSerializer


class SuppliersViewSet(viewsets.ModelViewSet):
    queryset = NetworkNode.objects.all()
    serializer_class = NetworkNodeSerializer

