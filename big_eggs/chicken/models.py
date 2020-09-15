import uuid

from dateutil.relativedelta import relativedelta
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils import timezone

from tenants.models import TenantDataModel

from .utils import today_midnight


class ChickenGroup(TenantDataModel):
    name = models.CharField(max_length=60)
    selectable = models.BooleanField(
        "Auswählbar",
        default=True,
        help_text="Gruppe auswählbar bei der Eingabe von Eiern?",
    )

    class Meta:
        ordering = ("name",)
        verbose_name = "Hühnergruppe"
        verbose_name_plural = "Hühnergruppen"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("chickengroup_update", kwargs={"pk": self.pk})

    def get_members(self):
        return self.chicken_set.all()


class Chicken(TenantDataModel):
    number = models.CharField("Ringnummer", max_length=60, blank=True,)
    name = models.CharField(max_length=60, blank=True)
    group = models.ForeignKey(
        ChickenGroup,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Gruppe",
    )
    hatching = models.DateTimeField("Schlupf", default=today_midnight)
    entry = models.DateTimeField("Zugang", default=today_midnight)
    departure = models.DateTimeField("Abgang", blank=True, null=True)

    SEX_CHOICES = [
        ("U", "---"),
        ("W", "♀"),
        ("M", "♂"),
    ]

    sex = models.CharField("Geschlecht", max_length=1, default="U", choices=SEX_CHOICES)
    note = models.TextField("Notizen", blank=True)

    class Meta:
        verbose_name = "Huhn"
        verbose_name_plural = "Hühner"

    def __str__(self):
        return self.name or self.number or str(self.id)

    def get_absolute_url(self):
        return reverse("chicken_update", kwargs={"pk": self.pk})

    def clean(self):
        errors = {}
        if self.departure and self.departure < self.entry:
            errors["departure"] = "Abgang kann nicht vor Zugang liegen."
        if self.entry < self.hatching:
            errors["entry"] = "Zugang kann nicht vor Schlupf liegen."
        if errors:
            raise ValidationError(errors)

    def age(self):
        until = self.departure or timezone.now()
        return relativedelta(until, self.hatching)


class Egg(TenantDataModel):
    laid = models.DateTimeField("Legedatum", default=today_midnight)
    group = models.ForeignKey(
        ChickenGroup,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        verbose_name="Gruppe",
    )
    chicken = models.ForeignKey(
        Chicken, blank=True, null=True, on_delete=models.CASCADE,
    )
    quantity = models.PositiveIntegerField("Anzahl", default=1)

    class Error(models.TextChoices):
        NONE = "N", "keine"
        BAUCH = "B", "Bauchei"
        DOPPEL = "D", "Doppeldotter"
        EI_IM_EI = "E", "Ei im Ei"
        KALK = "A", "Kalkablagerungen"
        KNICK = "K", "Knickei"
        WIND = "W", "Windei"
        SPAR = "S", "Sparei"
        SPUR = "P", "Spurei"
        BROKEN = "Z", "Zerstört"

    error = models.CharField("Fehler", default="N", max_length=1, choices=Error.choices)

    class Size(models.TextChoices):
        NONE = "N", "---------"
        S = "S", "S"
        M = "M", "M"
        L = "L", "L"
        XL = "X", "XL"

    size = models.CharField("Größe", default="N", max_length=1, choices=Size.choices)

    class Meta:
        ordering = ("-laid",)
        verbose_name = "Egg"
        verbose_name_plural = "Eggs"

    def __str__(self):
        out = "Eintrag vom {:%d.%m.%Y} mit {} Eiern".format(
            timezone.localdate(self.laid), self.quantity
        )
        if self.group:
            out += f" Gruppe: {self.group.name}"
        if self.error != "N":
            out += f" Fehler: {self.get_error_display()}"
        if self.size != "N":
            out += f" Größe: {self.get_size_display()}"
        return out

    @classmethod
    def get_size_definitions():
        return ["S: < 53g", "M: 53 =< 63g", "L: 63 =< 73g", "XL: > 73g"]
