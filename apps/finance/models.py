from django.db import models
from django.utils.translation import gettext_lazy as _


class Expense(models.Model):
    class Category(models.TextChoices):
        ADS = 'ads', _('Advertising')
        PRODUCTION = 'production', _('Production')
        TOOLS = 'tools', _('Tools')
        OTHER = 'other', _('Other')

    campaign = models.ForeignKey(
        'pipeline.Campaign', on_delete=models.CASCADE, related_name='expenses'
    )
    amount = models.DecimalField(_('Amount'), max_digits=12, decimal_places=2)
    category = models.CharField(
        _('Category'), max_length=12, choices=Category.choices, default=Category.ADS
    )
    date = models.DateField(_('Date'))

    class Meta:
        verbose_name = _('Expense')
        verbose_name_plural = _('Expenses')
        ordering = ['-date']


class Revenue(models.Model):
    campaign = models.ForeignKey(
        'pipeline.Campaign', on_delete=models.CASCADE, related_name='revenues'
    )
    amount = models.DecimalField(_('Amount'), max_digits=12, decimal_places=2)
    source = models.CharField(_('Source'), max_length=120, blank=True)
    date = models.DateField(_('Date'))

    class Meta:
        verbose_name = _('Revenue')
        verbose_name_plural = _('Revenues')
        ordering = ['-date']
