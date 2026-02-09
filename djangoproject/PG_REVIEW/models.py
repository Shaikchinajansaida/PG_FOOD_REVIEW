from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.

# -------------------------
# Owner Profile
# -------------------------
class OwnerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    is_owner = models.BooleanField(default=True)

    def __str__(self):
        return f"Owner: {self.user.username}"


# -------------------------
# PG / Hotel Listing
# -------------------------

TENANT_CHOICES = [
    ("family", "Family"),
    ("bachelor_male", "Bachelor Male"),
    ("bachelor_female", "Bachelor Female"),
    ("company", "Company"),
]

AVAIL_CHOICES = [
    ("immediate", "Immediate"),
    ("15", "Within 15 Days"),
    ("30", "Within 30 Days"),
    ("later", "After 30 Days"),
]

class PG(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="pgs")

    name = models.CharField(max_length=150)
    description = models.TextField()

    address = models.TextField()
    area = models.CharField(max_length=100)
    city = models.CharField(max_length=100)

    monthly_rent = models.PositiveIntegerField()
    food_available = models.BooleanField(default=True)

    image = models.ImageField(upload_to="pg_images/", blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    availability = models.CharField(
        max_length=20,
        choices=AVAIL_CHOICES,
        blank=True
    )

    tenant_type = models.CharField(
        max_length=30,
        choices=TENANT_CHOICES,
        blank=True
    )

    def __str__(self):
        return self.name

    @property
    def average_rating(self):
        reviews = self.reviews.all()
        if not reviews:
            return 0
        return round(sum(r.rating for r in reviews) / len(reviews), 2)

class PGImage(models.Model):
    pg = models.ForeignKey(
        PG,
        on_delete=models.CASCADE,
        related_name="images"
    )
    image = models.ImageField(upload_to="pg_images/")

    def __str__(self):
        return f"Image for {self.pg.name}"



# -------------------------
# Reviews / Ratings
# -------------------------
class Review(models.Model):
    pg = models.ForeignKey(PG, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    comment = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("pg", "user")  # one review per user per PG

    def __str__(self):
        return f"{self.pg.name} — {self.rating}⭐"
