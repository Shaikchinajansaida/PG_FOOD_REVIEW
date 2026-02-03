from django.contrib import admin
from .models import OwnerProfile, PG, Review

# Register your models here.

admin.site.register(OwnerProfile)
admin.site.register(PG)
admin.site.register(Review)