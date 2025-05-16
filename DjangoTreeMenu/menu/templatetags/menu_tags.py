from django import template
from django.template.loader import render_to_string

from menu.forms import CreateMenuItemForm

register = template.Library()


@register.simple_tag(takes_context=True)
def draw_menu(context, current_menu_id: int | None, current_menu_level: int, csrf_token):
    return render_to_string("menu/templatetags/draw_menu.html", {
        "request": context.get("request"),
        "father_id": current_menu_id,
        "current_menu_child_level": current_menu_level + 1,
        "form": CreateMenuItemForm,
        "csrf_token": csrf_token,
    })
