from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Angle, Creative, Hook


@login_required
def index(request):
    return render(request, 'assets/index.html', {
        'angles': Angle.objects.all(),
        'creatives': Creative.objects.select_related('angle', 'campaign')[:50],
        'hooks': Hook.objects.select_related('angle')[:50],
    })
