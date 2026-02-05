from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from .models import PG
from django.shortcuts import redirect
from .forms import ReviewForm
from .models import PG, Review
from django.contrib.auth import login
from .forms import ReviewForm, RegisterForm, PGForm
from .models import OwnerProfile
from .models import PG, OwnerProfile
from django.http import HttpResponseForbidden




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


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()

            # ✅ create owner profile if selected
            if form.cleaned_data.get("is_owner"):
                OwnerProfile.objects.create(
                    user=user,
                    phone=form.cleaned_data.get("phone"),
                    is_owner=True
                )

            login(request, user)
            return redirect("pg_list")

    else:
        form = RegisterForm()

    return render(request, "registration/register.html", {"form": form})

def owner_required(view_func):
    @login_required
    def _wrapped(request, *args, **kwargs):
        if not OwnerProfile.objects.filter(user=request.user, is_owner=True).exists():
            return HttpResponseForbidden("Owner access only")
        return view_func(request, *args, **kwargs)
    return _wrapped


@owner_required
def owner_dashboard(request):
    pgs = PG.objects.filter(owner=request.user).order_by("-created_at")

    return render(request, "pg_reviews/owner_dashboard.html", {
        "pgs": pgs
    })


@owner_required
def pg_edit(request, pg_id):

    pg = get_object_or_404(PG, id=pg_id, owner=request.user)

    form = PGForm(request.POST or None, instance=pg)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("owner_dashboard")

    return render(request, "pg_reviews/pg_form.html", {
        "form": form
    })

@owner_required
def pg_delete(request, pg_id):

    pg = get_object_or_404(PG, id=pg_id, owner=request.user)

    if request.method == "POST":
        pg.delete()
        return redirect("owner_dashboard")

    return render(request, "pg_reviews/pg_delete.html", {
        "pg": pg
    })

@owner_required
def pg_create(request):

    form = PGForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        pg = form.save(commit=False)
        pg.owner = request.user
        pg.save()
        return redirect("owner_dashboard")

    return render(request, "pg_reviews/pg_form.html", {
        "form": form
    })
