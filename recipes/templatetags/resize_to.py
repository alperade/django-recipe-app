from django import template

register = template.Library()


@register.filter
def resize_to(ingredient, target):
    num_servings = int(ingredient.recipe.serving)
    amount = int(ingredient.amount)
    if num_servings is not None and target is not None:
        new_serv_amount = int(target) * amount / num_servings
        return new_serv_amount
    else:
        return amount
