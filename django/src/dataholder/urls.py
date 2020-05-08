from django.urls import path, include

# api - location of all REST API interfaces
urlpatterns = [
    path('api/', include(("dataholder.api.urls",'api'), namespace='api')),
]

