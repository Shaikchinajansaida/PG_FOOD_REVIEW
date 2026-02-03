from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from .models import PG
# Create your views here.
def index(request):
    return HttpResponse("Hello, welcome to the PG Food Review App!")


def pg_list(request):
    pgs = PG.objects.all().order_by("-created_at")

    return render(request, "pg_reviews/pg_list.html", {
        "pgs": pgs
    })

def pg_detail(request, pg_id):
    pg = get_object_or_404(PG, id=pg_id)

    reviews = pg.reviews.select_related("user").all().order_by("-created_at")

    context = {
        "pg": pg,
        "reviews": reviews,
    }

    return render(request, "pg_reviews/pg_detail.html", context)