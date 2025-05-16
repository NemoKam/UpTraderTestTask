from django import forms
from django.contrib import admin

from menu.models import MenuItem


class MenuItemInlineForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = "__all__"


class MenuItemInline(admin.TabularInline):
    model = MenuItem
    form = MenuItemInlineForm
    verbose_name_plural = "Menu sub-items"
    extra = 1


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    inlines = [MenuItemInline]

    list_display = ("title", "father__title")
    search_fields = ("title",)
    list_filter = ("father",)
    ordering = ("title",)
    list_per_page = 20
