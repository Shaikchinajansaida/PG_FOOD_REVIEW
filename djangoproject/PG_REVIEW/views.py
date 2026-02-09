from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.db.models import Q

from .models import PG, Review, OwnerProfile, PGImage
from .forms import ReviewForm, RegisterForm, PGForm


# Create your views here.
def index(request):
    return redirect("pg_list")


def pg_list(request):
    pgs = PG.objects.all().order_by("-created_at")

    q = request.GET.get("q")
    if q:
        pgs = pgs.filter(
            Q(name__icontains=q) |
            Q(city__icontains=q) |
            Q(area__icontains=q)
        )

    # -------- PRICE RANGE --------
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")

    if min_price:
        pgs = pgs.filter(monthly_rent__gte=min_price)

    if max_price:
        pgs = pgs.filter(monthly_rent__lte=max_price)

    # -------- AVAILABILITY --------
    avail = request.GET.get("availability")
    if avail:
        pgs = pgs.filter(availability=avail)

    # -------- TENANT TYPE --------
    tenant = request.GET.get("tenant")
    if tenant:
        pgs = pgs.filter(tenant_type=tenant)

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

            #  create owner profile if selected
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

    form = PGForm(request.POST or None, request.FILES or None, instance=pg)

    if request.method == "POST" and form.is_valid():
        pg = form.save()

        #  handle extra images on edit too
        files = request.FILES.getlist("images")
        for f in files:
            PGImage.objects.create(pg=pg, image=f)

        return redirect("owner_dashboard")

    return render(request, "pg_reviews/pg_form.html", {"form": form})


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

    form = PGForm(request.POST or None, request.FILES or None)

    if request.method == "POST" and form.is_valid():
        pg = form.save(commit=False)
        pg.owner = request.user
        pg.save()

        #  handle multiple images
        files = request.FILES.getlist("images")

        for f in files:
            PGImage.objects.create(pg=pg, image=f)

        return redirect("owner_dashboard")

    return render(request, "pg_reviews/pg_form.html", {
        "form": form
    })