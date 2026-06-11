from django.db import models
from django.utils.translation import gettext_lazy as _


class Angle(models.Model):
    class Category(models.TextChoices):
        PROBLEM_SOLUTION = 'problem_solution', _('Problem / Solution')
        BENEFIT = 'benefit', _('Benefit')
        OFFER = 'offer', _('Irresistible Offer')

    name = models.CharField(_('Name'), max_length=120)
    category = models.CharField(
        _('Category'), max_length=32, choices=Category.choices,
        default=Category.BENEFIT,
    )
    success_rate = models.FloatField(_('Success rate (%)'), default=0)

    class Meta:
        verbose_name = _('Angle')
        verbose_name_plural = _('Angles')

    def __str__(self):
        return self.name


class Creative(models.Model):
    class MediaType(models.TextChoices):
        IMAGE = 'image', _('Image')
        VIDEO = 'video', _('Video')

    title = models.CharField(_('Title'), max_length=160)
    campaign = models.ForeignKey(
        'pipeline.Campaign', on_delete=models.CASCADE, related_name='creatives',
        null=True, blank=True,
    )
    angle = models.ForeignKey(
        Angle, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='creatives',
    )
    file = models.FileField(_('File'), upload_to='creatives/', null=True, blank=True)
    media_type = models.CharField(
        _('Type'), max_length=8, choices=MediaType.choices, default=MediaType.IMAGE,
    )
    is_winner = models.BooleanField(_('Winner?'), default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Creative')
        verbose_name_plural = _('Creatives')
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    @property
    def file_is_video(self):
        return bool(self.file and self.file.name.lower().endswith(('.mp4', '.webm', '.mov', '.m4v')))

    @property
    def file_is_image(self):
        return bool(self.file and self.file.name.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg')))


class Hook(models.Model):
    class Platform(models.TextChoices):
        SOCIAL = 'social', _('Social Media')
        SEARCH = 'search', _('Search')
        DISPLAY = 'display', _('Display')

    class Trigger(models.TextChoices):
        CURIOSITY = 'curiosity', _('Curiosity')
        PAIN = 'pain', _('Pain Point')
        DEMO = 'demo', _('Demonstration')

    text = models.TextField(_('Text'))
    platform = models.CharField(_('Platform'), max_length=10, choices=Platform.choices)
    trigger_type = models.CharField(_('Trigger'), max_length=10, choices=Trigger.choices)
    angle = models.ForeignKey(
        Angle, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='hooks',
    )
    performance_score = models.FloatField(_('Performance score'), default=0)

    class Meta:
        verbose_name = _('Hook')
        verbose_name_plural = _('Hooks')

    def __str__(self):
        return self.text[:60]
