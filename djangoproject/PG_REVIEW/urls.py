from django.urls import path
from .views import pg_list
from .views import pg_detail
from .views import review_create



urlpatterns = [
    path("pgs/", pg_list, name="pg_list"),
    path("pg/<int:pg_id>/", pg_detail, name="pg_detail"),
    path("pg/<int:pg_id>/review/add/", review_create, name="review_add"),
]

