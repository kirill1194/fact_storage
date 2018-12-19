from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from django.shortcuts import get_object_or_404
from apps.storage.models import Fact
from .serializer import FactSerializer

class FactListViewset(ReadOnlyModelViewSet):
    model = Fact
    paginate_by = 10
    queryset = Fact.objects.all()

    def list(self, request):
        queryset = Fact.objects.all()
        serializer = FactSerializer(queryset, many=True)

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Fact.objects.all()
        fact = get_object_or_404(queryset, uuid=pk)
        serializer = FactSerializer(fact)

        return Response(serializer.data)