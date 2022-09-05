from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.db import IntegrityError

from recipes.forms import RatingForm

from recipes.models import Recipe, ShoppingItem, Ingredient
from django.contrib.auth import get_user_model


def log_rating(request, recipe_id):
    if request.method == "POST":
        form = RatingForm(request.POST)
        if form.is_valid():
            try:
                rating = form.save(commit=False)
                rating.recipe = Recipe.objects.get(pk=recipe_id)
                rating.save()
            except Recipe.DoesNotExist:
                return redirect("recipes_list")
        return redirect("recipe_detail", pk=recipe_id)


class RecipeListView(ListView):
    model = Recipe
    template_name = "recipes/list.html"
    paginate_by = 2


class RecipeDetailView(DetailView):
    model = Recipe
    template_name = "recipes/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["rating_form"] = RatingForm()
        foods = []
        for item in self.request.user.shopping_items.all():
            foods.append(item.food_item)
        context["food_in_shopping_list"] = foods
        context["serving"] = self.request.GET.get("serving")
        return context


class RecipeCreateView(LoginRequiredMixin, CreateView):
    model = Recipe
    template_name = "recipes/new.html"
    fields = ["name", "description", "serving", "image"]
    success_url = reverse_lazy("recipes_list")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class RecipeUpdateView(LoginRequiredMixin, UpdateView):
    model = Recipe
    template_name = "recipes/edit.html"
    fields = ["name", "author", "description", "serving", "image"]
    success_url = reverse_lazy("recipes_list")


class RecipeDeleteView(LoginRequiredMixin, DeleteView):
    model = Recipe
    template_name = "recipes/delete.html"
    success_url = reverse_lazy("recipes_list")


@require_http_methods(["POST"])
def shopping_item_create(request):
    ingredient_id = request.POST.get("ingredient_id")
    ingredient = Ingredient.objects.get(id=ingredient_id)
    user = request.user

    try:
        ShoppingItem.objects.create(food_item=ingredient.food, user=user)
    except IntegrityError:
        pass
    return redirect("recipe_detail", pk=ingredient.recipe.id)


@login_required(login_url="/login")
def shopping_items_list(request):
    user = request.user
    shopping_items = ShoppingItem.objects.filter(user=user)
    context = {"shopping_items": shopping_items}
    response = render(request, "recipes/shopping_items.html", context)
    return response


@require_http_methods(["POST"])
def shopping_item_delete(request):
    user = request.user
    try:
        ShoppingItem.objects.filter(user=user).all().delete()
    except IntegrityError:
        pass
    return redirect("shopping_items")


def users_and_recipes(request):
    User = get_user_model()
    users = User.objects.all()
    library = Recipe.objects.all()
    context = {
        "user_list": users,
        "library": library,
    }
    response = render(request, "recipes/users_and_recipes.html", context)
    return response
