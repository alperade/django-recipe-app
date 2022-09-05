from django.urls import path

from meal_plans.views import (
    MealPlanCreateView,
    MealPlanDeleteView,
    MealPlanUpdateView,
    MealPlanListView,
    MealPlanDetailView,
)

urlpatterns = [
    path("", MealPlanListView, name="meal_plans_list"),
    path(
        "<int:pk>/delete/",
        MealPlanDeleteView,
        name="meal_plan_delete",
    ),
    path("create/", MealPlanCreateView, name="meal_plan_create"),
    path(
        "<int:pk>/edit/",
        MealPlanUpdateView,
        name="meal_plan_edit",
    ),
    path("<int:pk>/", MealPlanDetailView, name="meal_plan_detail"),
]
