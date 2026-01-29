from django.contrib import admin

# Register your models here.
from .models import PG, Review

admin.site.register(PG)
admin.site.register(Review)
