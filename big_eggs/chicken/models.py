import uuid

from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.core.exceptions import ValidationError


def today_midnight():
    return timezone.localtime(timezone.now()).replace(hour=0, minute=0, second=0, microsecond=0)


class ChickenGroup(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=60, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('chickengroup_update', kwargs={'pk': self.pk})

    def get_members(self):
        return self.chicken_set.all()


class Chicken(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    number = models.CharField('Ringnummer', max_length=60, blank=True, )
    name = models.CharField(max_length=60, blank=True)
    group = models.ForeignKey(ChickenGroup,
                              blank=True, null=True, on_delete=models.SET_NULL,
                              verbose_name='Gruppe')
    hatching = models.DateTimeField('Schlupf', default=today_midnight)
    entry = models.DateTimeField('Zugang', default=today_midnight)
    departure = models.DateTimeField('Abgang', blank=True, null=True)

    SEX_CHOICES = [
        ('U', '---'),
        ('W', '♀'),
        ('M', '♂'),
    ]

    sex = models.CharField('Geschlecht', max_length=1,
                           default='U', choices=SEX_CHOICES)
    note = models.TextField('Notizen', blank=True)

    def __str__(self):
        return self.name or self.number or str(self.id)

    def get_absolute_url(self):
        return reverse('chicken_update', kwargs={'pk': self.pk})

    def clean(self):
        if self.departure and self.departure < self.entry:
            raise ValidationError({
                'departure': 'Abgang kann nicht vor Zugang liegen.'
            })
        if self.entry <= self.hatching:
            raise ValidationError({
                'entry': 'Zugang kann nicht vor Schlupf liegen.'
            })

class Egg(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    laid = models.DateTimeField(default=today_midnight)
    group = models.ForeignKey(ChickenGroup,
                              blank=True, null=True, on_delete=models.CASCADE)
    chicken = models.ForeignKey(Chicken,
                                blank=True, null=True, on_delete=models.CASCADE)

    DEFORMITY_CHOICES = (
        ('W', 'Windei'),
        ('Z', 'Zerstört'),
    )
    errors = models.CharField('Fehler', blank=True,
                              max_length=1, choices=DEFORMITY_CHOICES)

    class Meta:
        ordering = ('-laid',)
        verbose_name = 'Egg'
        verbose_name_plural = 'Eggs'

    def __str__(self):
        return 'Ei vom {:%d.%m.%Y}'.format(self.laid)
