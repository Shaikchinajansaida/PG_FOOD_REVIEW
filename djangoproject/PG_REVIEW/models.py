from django.db import models

# Create your models here.
from django.core.validators import MinValueValidator, MaxValueValidator


class PG(models.Model):
    name = models.CharField(max_length=150)
    location = models.CharField(max_length=200)
    price_per_month = models.PositiveIntegerField()
    food_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Review(models.Model):
    pg = models.ForeignKey(PG, on_delete=models.CASCADE, related_name="reviews")
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.pg.name} - {self.rating}⭐"
