from django.urls import path
from .views import pg_list
from .views import pg_detail
from .views import review_create
from . import views



urlpatterns = [
    path("pgs/", pg_list, name="pg_list"),
    path("pg/<int:pg_id>/", pg_detail, name="pg_detail"),
    path("pg/<int:pg_id>/review/add/", review_create, name="review_add"),
    path("register/", views.register_view, name="register"),
    path("owner/dashboard/", views.owner_dashboard, name="owner_dashboard"),
    path("pg/<int:pg_id>/edit/", views.pg_edit, name="pg_edit"),
    path("pg/<int:pg_id>/delete/", views.pg_delete, name="pg_delete"),
    path("pg/create/", views.pg_create, name="pg_create"),
]

