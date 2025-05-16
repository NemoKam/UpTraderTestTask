from django.urls import path, re_path

from menu.views import MenuView

app_name = "menu"


urlpatterns = [
    path("", MenuView.as_view(), name="menu_base_view"),
    re_path(r"^(?P<path>.*)/$", MenuView.as_view(), name="menu_view"),
]
