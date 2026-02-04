from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from .models import PG
from django.shortcuts import redirect
from .forms import ReviewForm
from .models import PG, Review



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



@login_required
def review_create(request, pg_id):
    pg = get_object_or_404(PG, id=pg_id)

    if Review.objects.filter(pg=pg, user=request.user).exists():
        return redirect("pg_detail", pg_id=pg.id)

    form = ReviewForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        review = form.save(commit=False)
        review.pg = pg
        review.user = request.user
        review.save()
        return redirect("pg_detail", pg_id=pg.id)

    return render(request, "pg_reviews/review_form.html", {
        "form": form,
        "pg": pg
    })
