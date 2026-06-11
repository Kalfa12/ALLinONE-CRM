from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import redirect, render

from apps.pipeline.models import Campaign

from .models import Expense, Revenue


@login_required
def dashboard(request):
    rows = []
    for c in Campaign.objects.all():
        spent = c.total_spent()
        revenue = c.total_revenue()
        roi = c.roi()
        rows.append({
            'campaign': c,
            'budget': c.budget,
            'spent': spent,
            'revenue': revenue,
            'roi': roi,
        })
    total_spent = sum((r['spent'] for r in rows), Decimal('0'))
    total_revenue = sum((r['revenue'] for r in rows), Decimal('0'))
    roi_values = [r['roi'] for r in rows if r['roi'] is not None]
    totals = {
        'spent': total_spent,
        'revenue': total_revenue,
        'profit': total_revenue - total_spent,
        'average_roi': sum(roi_values) / len(roi_values) if roi_values else None,
        'campaigns': len(rows),
    }
    return render(request, 'finance/dashboard.html', {
        'rows': rows,
        'totals': totals,
    })


@login_required
def expense_create(request):
    if request.method == 'POST':
        Expense.objects.create(
            campaign_id=request.POST['campaign'],
            amount=request.POST['amount'],
            category=request.POST.get('category', 'ads'),
            date=request.POST['date'],
        )
        return redirect('finance:dashboard')
    return render(request, 'finance/expense_form.html', {
        'campaigns': Campaign.objects.all(),
        'categories': Expense.Category.choices,
    })


@login_required
def revenue_create(request):
    if request.method == 'POST':
        Revenue.objects.create(
            campaign_id=request.POST['campaign'],
            amount=request.POST['amount'],
            source=request.POST.get('source', ''),
            date=request.POST['date'],
        )
        return redirect('finance:dashboard')
    return render(request, 'finance/revenue_form.html', {
        'campaigns': Campaign.objects.all(),
    })
