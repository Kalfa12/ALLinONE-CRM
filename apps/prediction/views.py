from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import PredictionLog
from .services import predict_potential

CATEGORIES = ['beauty', 'fashion', 'tech', 'home', 'fitness', 'food']
ANGLES = ['problem_solution', 'benefit', 'offer']
COMPETITION = ['low', 'medium', 'high']


@login_required
def form(request):
    result = None
    error = None

    if request.method == 'POST':
        features = {
            'category': request.POST.get('category'),
            'price': float(request.POST.get('price') or 0),
            'competition_level': request.POST.get('competition_level'),
            'angle_type': request.POST.get('angle_type'),
            'initial_ctr': float(request.POST.get('initial_ctr') or 0),
        }
        try:
            cls, conf = predict_potential(features)
            PredictionLog.objects.create(
                user=request.user,
                input_features=features,
                predicted_class=cls,
                confidence=conf,
            )
            result = {'class': cls, 'confidence': conf, 'features': features}
        except FileNotFoundError as e:
            error = str(e)

    return render(request, 'prediction/form.html', {
        'result': result,
        'error': error,
        'categories': CATEGORIES,
        'angles': ANGLES,
        'competition_levels': COMPETITION,
        'recent': PredictionLog.objects.filter(user=request.user)[:5],
    })
