from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User


from meal_plans.models import MealPlan


class MealPlanListView(LoginRequiredMixin, ListView):
    model = MealPlan
    template_name = "meal_plans/list.html"
    paginate_by = 2
    context_object_name = "mealplans"

    def get_queryset(self):
        return MealPlan.objects.filter(owner=self.request.user)


class MealPlanCreateView(LoginRequiredMixin, CreateView):
    model = MealPlan
    template_name = "meal_plans/create.html"
    fields = ["name", "date", "recipes"]
    success_url = reverse_lazy("meal_plans_list")

    def form_valid(self, form):
        plan = form.save(commit=False)
        plan.owner = self.request.user
        plan.save()
        form.save_m2m()
        return redirect("meal_plan_detail", pk=plan.id)


class MealPlanUpdateView(LoginRequiredMixin, UpdateView):
    model = MealPlan
    template_name = "meal_plans/edit.html"
    fields = ["name", "date", "recipes"]
    success_url = reverse_lazy("meal_plans_list")


class MealPlanDeleteView(LoginRequiredMixin, DeleteView):
    model = MealPlan
    template_name = "meal_plans/delete.html"
    success_url = reverse_lazy("meal_plans_list")
    context_object_name = "meal_plan"


class MealPlanDetailView(LoginRequiredMixin, DetailView):
    model = MealPlan
    template_name = "meal_plans/detail.html"
    context_object_name = "meal_plan"
