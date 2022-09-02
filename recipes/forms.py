from django import forms

from recipes.models import Recipe


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = [
            "name",
            "author",
            "description",
            "serving",
            "image",
        ]


from recipes.models import Rating


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ["value"]
