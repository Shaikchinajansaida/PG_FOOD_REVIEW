from django.urls import path
from .views import pg_list
from .views import pg_detail


urlpatterns = [
    path("pgs/", pg_list, name="pg_list"),
    path("pg/<int:pg_id>/", pg_detail, name="pg_detail"),
]

