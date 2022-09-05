from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from meal_plans.models import MealPlan
from meal_plans.forms import MealPlanForm, MealPlanDeleteForm


@login_required
def MealPlanListView(request):
    context = {"mealplans": MealPlan.objects.filter(owner=request.user)}

    return render(request, "meal_plans/list.html", context)


@login_required
def MealPlanCreateView(request):
    if request.method == "POST":
        form = MealPlanForm(request.POST)
        if form.is_valid():
            plan = form.save(commit=False)
            plan.owner = request.user
            plan.save()
            form.save_m2m()
            return redirect("meal_plan_detail", pk=plan.id)
    else:
        form = MealPlanForm()
    context = {"form": form}
    return render(
        request,
        "meal_plans/create.html",
        context,
    )


@login_required
def MealPlanUpdateView(request, pk):
    plan = MealPlan.objects.filter(owner=request.user).get(pk=pk)
    if request.method == "POST":
        form = MealPlanForm(request.POST, instance=plan)
        if form.is_valid():
            plan = form.save(commit=False)
            plan.owner = request.user
            plan.save()
            form.save_m2m()
            return redirect("meal_plan_detail", pk=plan.id)
    else:
        form = MealPlanForm(instance=plan)
    context = {"form": form}
    return render(request, "meal_plans/edit.html", context)


@login_required
def MealPlanDetailView(request, pk):
    context = {
        "meal_plan": MealPlan.objects.filter(owner=request.user).get(pk=pk)
    }
    return render(request, "meal_plans/detail.html", context)


@login_required
def MealPlanDeleteView(request, pk):
    plan = MealPlan.objects.filter(owner=request.user).get(pk=pk)
    if request.method == "POST":
        form = MealPlanDeleteForm(request.POST, instance=plan)
        if form.is_valid():
            plan.delete()
            return redirect("meal_plans_list")
    else:
        form = MealPlanDeleteForm(instance=plan)
    context = {
        "form": form,
        "meal_plan": plan,
    }
    return render(request, "meal_plans/delete.html", context)
