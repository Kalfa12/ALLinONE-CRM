from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from apps.pipeline.models import Campaign

from .forms import ExpenseForm, RevenueForm
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
        'expenses': Expense.objects.select_related('campaign', 'campaign__product')[:25],
        'revenues': Revenue.objects.select_related('campaign', 'campaign__product')[:25],
        'totals': totals,
    })


@login_required
@require_http_methods(['GET', 'POST'])
def expense_create(request):
    form = ExpenseForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('finance:dashboard')
    return render(request, 'finance/finance_form.html', {
        'form': form,
        'title': 'Log expense',
        'submit_label': 'Save expense',
        'tone': 'rose',
    })


@login_required
@require_http_methods(['GET', 'POST'])
def expense_update(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    form = ExpenseForm(request.POST or None, instance=expense)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('finance:dashboard')
    return render(request, 'finance/finance_form.html', {
        'form': form,
        'title': 'Edit expense',
        'submit_label': 'Save changes',
        'tone': 'rose',
    })


@login_required
@require_http_methods(['GET', 'POST'])
def expense_delete(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    if request.method == 'POST':
        expense.delete()
        return redirect('finance:dashboard')
    return render(request, 'confirm_delete.html', {
        'object': expense,
        'object_type': 'expense',
        'cancel_href': '/finance/',
    })


@login_required
@require_http_methods(['GET', 'POST'])
def revenue_create(request):
    form = RevenueForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('finance:dashboard')
    return render(request, 'finance/finance_form.html', {
        'form': form,
        'title': 'Log revenue',
        'submit_label': 'Save revenue',
        'tone': 'emerald',
    })


@login_required
@require_http_methods(['GET', 'POST'])
def revenue_update(request, pk):
    revenue = get_object_or_404(Revenue, pk=pk)
    form = RevenueForm(request.POST or None, instance=revenue)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('finance:dashboard')
    return render(request, 'finance/finance_form.html', {
        'form': form,
        'title': 'Edit revenue',
        'submit_label': 'Save changes',
        'tone': 'emerald',
    })


@login_required
@require_http_methods(['GET', 'POST'])
def revenue_delete(request, pk):
    revenue = get_object_or_404(Revenue, pk=pk)
    if request.method == 'POST':
        revenue.delete()
        return redirect('finance:dashboard')
    return render(request, 'confirm_delete.html', {
        'object': revenue,
        'object_type': 'revenue',
        'cancel_href': '/finance/',
    })
