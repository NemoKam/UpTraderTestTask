from typing import Optional

from django.db import models

from menu.validators import no_slash_validator


class MenuItem(models.Model):
    """MenuItem model."""

    title = models.CharField(
        "Menu title",
        validators=[no_slash_validator],
        max_length=256,
        null=False,
        blank=False,
    )
    father: Optional["MenuItem"] = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Menu item"
        verbose_name_plural = "Menu items"
        db_table = "menu_menuitem"

    def __str__(self):
        return self.title
