import json

from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters
from rest_framework.response import Response
from rest_framework.status   import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.generics import (
   ListAPIView,
   RetrieveAPIView,
)

from .serializers import MatchSerializer

from dataholder.models import (
    Match,
    Score,
    Team,
)

##########################################
class MatchFilter(filters.FilterSet):
    min_date_start = filters.NumberFilter(field_name="date_start", lookup_expr='gte')
    max_date_start = filters.NumberFilter(field_name="date_start", lookup_expr='lte')

    class Meta:
        model = Match
        fields = ['title', 'tournament_name','state','min_date_start','max_date_start']


##########################################
class ListView(ListAPIView):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer

    #Enable filtering : title, tournament, state, date_start__gte and date_start_lte
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = MatchFilter
   


##########################################
class DetailsView(RetrieveAPIView):
    queryset = Match.objects.all()
    lookup_url_kwarg = 'dj_id'
    serializer_class = MatchSerializer

