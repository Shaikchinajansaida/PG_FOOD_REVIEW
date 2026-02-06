from django import forms
from .models import Review
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import PG


class ReviewForm(forms.ModelForm):

    rating = forms.ChoiceField(
        choices=[(1,"1"), (2,"2"), (3,"3"), (4,"4"), (5,"5")],
        label="Rating"
    )

    class Meta:
        model = Review
        fields = ["rating", "comment"]

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=15, required=False)
    is_owner = forms.BooleanField(
        required=False,
        label="Register as PG Owner"
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class PGForm(forms.ModelForm):
    class Meta:
        model = PG
        fields = [
            "name",
            "description",
            "address",
            "area",
            "city",
            "monthly_rent",
            "food_available",
            "image",
        ]