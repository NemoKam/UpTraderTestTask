from django import forms

from menu.models import MenuItem


class CreateMenuItemForm(forms.ModelForm):
    father_id = forms.IntegerField()

    class Meta:
        model = MenuItem
        fields = "__all__"
        exclude = ("father",)
