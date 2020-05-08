from django.urls import path, include
from dataholder.api.views import ListView, DetailsView

urlpatterns = [
    path('list/',               ListView.as_view(),    name='list'),
    path('detail/<int:dj_id>/', DetailsView.as_view(), name='detail'),
]
