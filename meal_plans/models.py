from django.db import models
from django.conf import settings

USER_MODEL = settings.AUTH_USER_MODEL


class MealPlan(models.Model):
    name = models.CharField(max_length=120)
    date = models.DateTimeField(auto_now=False, auto_now_add=False)
    owner = models.ForeignKey(
        USER_MODEL, related_name=("owner"), on_delete=models.CASCADE
    )
    recipes = models.ManyToManyField("recipes.Recipe", related_name=("recipes"))

    def __str__(self):
        return self.name
