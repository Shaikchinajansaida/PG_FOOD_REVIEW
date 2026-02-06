from django.contrib import admin
from .models import OwnerProfile, PG, Review
from .models import PG, PGImage

# Register your models here.

admin.site.register(OwnerProfile)
# admin.site.register(PG)
admin.site.register(Review)
admin.site.register(PGImage)


class PGImageInline(admin.TabularInline):
    model = PGImage
    extra = 3


@admin.register(PG)
class PGAdmin(admin.ModelAdmin):
    inlines = [PGImageInline]
