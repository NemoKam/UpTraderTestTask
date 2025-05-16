from typing import TYPE_CHECKING
from urllib.parse import quote

from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic.list import ListView

from menu.forms import CreateMenuItemForm
from menu.models import MenuItem
from menu.services import get_menu_service

if TYPE_CHECKING:
    from menu.types import MenuTree


class MenuView(ListView):
    """Menu page."""

    template_name = "menu/index.html"
    model = MenuItem

    def get_context_data(self, **kwargs):
        """Return menu by path."""
        context = super().get_context_data(**kwargs)

        path: str = str(self.kwargs.get("path"))
        menu_tree: MenuTree = get_menu_service().get_menu_tree(path)

        context["current_menu_id"] = menu_tree.current_menu_id
        context["menu_items"] = menu_tree.tree_menu_items

        return context

    def post(self, request, *args, **kwargs):
        """Create menu item child."""
        create_menu_item_form = CreateMenuItemForm(self.request.POST)

        return_url = request.build_absolute_uri()
        if create_menu_item_form.is_valid():
            title = str(create_menu_item_form.cleaned_data.get("title"))
            father_id = int(create_menu_item_form.cleaned_data.get("father_id"))

            MenuItem.objects.create(title=title, father_id=father_id)

            return_url += quote(title, safe="")
        else:
            messages.error(request, str(create_menu_item_form.errors))

        return redirect(return_url)
