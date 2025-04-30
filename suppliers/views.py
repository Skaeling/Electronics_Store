from django_filters import rest_framework as filters
from rest_framework import viewsets
from .models import NetworkNode
from .serializers import NetworkNodeSerializer


class SuppliersViewSet(viewsets.ModelViewSet):
    queryset = NetworkNode.objects.all()
    serializer_class = NetworkNodeSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('contacts__country',)
