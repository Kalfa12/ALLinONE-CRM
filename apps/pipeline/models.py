from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class Product(models.Model):
    class Status(models.TextChoices):
        PLANNING = 'planning', _('Planning')
        ACTIVE = 'active', _('Active')
        EVALUATED = 'evaluated', _('Evaluated')

    name = models.CharField(_('Name'), max_length=120)
    description = models.TextField(_('Description'), blank=True)
    status = models.CharField(
        _('Status'), max_length=16, choices=Status.choices, default=Status.PLANNING
    )
    score = models.FloatField(_('Score'), default=0)
    notes = models.TextField(_('Notes'), blank=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='products',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class Campaign(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'draft', _('Draft')
        RUNNING = 'running', _('Running')
        DONE = 'done', _('Done')

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='campaigns'
    )
    name = models.CharField(_('Name'), max_length=120)
    start_date = models.DateField(_('Start date'))
    end_date = models.DateField(_('End date'), null=True, blank=True)
    budget = models.DecimalField(_('Budget'), max_digits=12, decimal_places=2, default=0)
    status = models.CharField(
        max_length=10, choices=Status.choices, default=Status.DRAFT
    )

    class Meta:
        verbose_name = _('Campaign')
        verbose_name_plural = _('Campaigns')
        ordering = ['-start_date']

    def __str__(self):
        return f'{self.product.name} — {self.name}'

    def total_spent(self):
        return self.expenses.aggregate(s=models.Sum('amount'))['s'] or 0

    def total_revenue(self):
        return self.revenues.aggregate(s=models.Sum('amount'))['s'] or 0

    def roi(self):
        spent = self.total_spent()
        if not spent:
            return None
        return float((self.total_revenue() - spent) / spent * 100)
