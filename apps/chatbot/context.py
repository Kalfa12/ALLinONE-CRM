"""Builds a compact, factual snapshot of the CRM to ground the chatbot."""
from django.db.models import Sum

from apps.assets.models import Angle
from apps.finance.models import Expense, Revenue
from apps.pipeline.models import Campaign, Product


def build_crm_context(user) -> str:
    parts = []

    counts = {
        s: Product.objects.filter(status=s).count()
        for s, _ in Product.Status.choices
    }
    parts.append(
        f"Products in pipeline — planning:{counts['planning']}, "
        f"active:{counts['active']}, evaluated:{counts['evaluated']}."
    )

    top_campaigns = Campaign.objects.all()[:5]
    if top_campaigns:
        parts.append('Recent campaigns:')
        for c in top_campaigns:
            roi = c.roi()
            roi_str = f'{roi:.1f}%' if roi is not None else 'n/a'
            parts.append(
                f'  - "{c.name}" (product: {c.product.name}) — '
                f'budget {c.budget} MAD, spent {c.total_spent()} MAD, '
                f'revenue {c.total_revenue()} MAD, ROI {roi_str}'
            )

    spent = Expense.objects.aggregate(s=Sum('amount'))['s'] or 0
    revenue = Revenue.objects.aggregate(s=Sum('amount'))['s'] or 0
    parts.append(f'Total spent: {spent} MAD — total revenue: {revenue} MAD.')

    angles = Angle.objects.order_by('-success_rate')[:3]
    if angles:
        parts.append(
            'Best angles: '
            + ', '.join(f'{a.name} ({a.success_rate:.0f}%)' for a in angles)
        )

    return '\n'.join(parts)
