import django.core.validators as v
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from tinymce.models import HTMLField


class Board(models.Model):
    """Represents a story board or plot board."""

    class Meta:
        verbose_name = _("board")
        verbose_name_plural = _("boards")

    name = models.CharField(_("name"), max_length=255)
    description = models.TextField(_("description"), blank=True, max_length=4000)
    per_row = models.PositiveSmallIntegerField(
        _("sequences per row"),
        validators=[v.MinValueValidator(1), v.MaxValueValidator(32)],
        default=2,
    )
    owner = models.ForeignKey("auth.user", on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("board_detail", kwargs={"pk": self.pk})


class Sequence(models.Model):
    """A Sequence is a container for Cards within a Board."""

    class Meta:
        verbose_name = _("sequence")
        verbose_name_plural = _("sequences")

    name = models.CharField(_("name"), max_length=255)
    description = models.TextField(_("description"), blank=True, max_length=4000)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Card(models.Model):
    class Meta:
        verbose_name = _("card")
        verbose_name_plural = _("cards")
        order_with_respect_to = "sequence"

    name = models.CharField(_("name"), max_length=255, blank=True)
    description = models.TextField(_("description"), blank=True, max_length=4000)
    content = HTMLField(_("content"), blank=True)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    sequence = models.ForeignKey(
        Sequence, on_delete=models.SET_NULL, blank=True, null=True
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("card_detail", kwargs={"pk": self.pk})
