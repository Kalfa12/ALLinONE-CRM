from django.utils.translation import gettext_lazy as _


def nav(request):
    """Inject the main navigation entries into every template."""
    active_namespace = getattr(getattr(request, 'resolver_match', None), 'namespace', '')
    return {
        'active_namespace': active_namespace,
        'nav_items': [
            {'url_name': 'pipeline:kanban', 'label': _('Pipeline'), 'namespace': 'pipeline', 'icon': 'kanban-square'},
            {'url_name': 'assets:index', 'label': _('Assets'), 'namespace': 'assets', 'icon': 'layers'},
            {'url_name': 'finance:dashboard', 'label': _('Finance'), 'namespace': 'finance', 'icon': 'line-chart'},
            {'url_name': 'prediction:form', 'label': _('Predict'), 'namespace': 'prediction', 'icon': 'sparkles'},
        ],
    }
