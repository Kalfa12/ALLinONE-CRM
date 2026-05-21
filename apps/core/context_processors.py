from django.utils.translation import gettext_lazy as _


def nav(request):
    """Inject the main navigation entries into every template."""
    return {
        'nav_items': [
            {'url_name': 'pipeline:kanban', 'label': _('Pipeline')},
            {'url_name': 'assets:index', 'label': _('Assets')},
            {'url_name': 'finance:dashboard', 'label': _('Finance')},
            {'url_name': 'prediction:form', 'label': _('Predict')},
        ],
    }
