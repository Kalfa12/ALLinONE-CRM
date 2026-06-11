from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods, require_POST

from .models import Campaign, Product


@login_required
def kanban(request):
    products_by_status = {
        status: list(Product.objects.filter(status=status))
        for status, _ in Product.Status.choices
    }
    all_products = [product for products in products_by_status.values() for product in products]
    average_score = (
        sum(product.score for product in all_products) / len(all_products)
        if all_products else 0
    )
    return render(request, 'pipeline/kanban.html', {
        'columns': [
            (Product.Status.PLANNING, products_by_status[Product.Status.PLANNING]),
            (Product.Status.ACTIVE, products_by_status[Product.Status.ACTIVE]),
            (Product.Status.EVALUATED, products_by_status[Product.Status.EVALUATED]),
        ],
        'metrics': {
            'products': len(all_products),
            'active': len(products_by_status[Product.Status.ACTIVE]),
            'campaigns': Campaign.objects.count(),
            'average_score': average_score,
        },
        'statuses': Product.Status,
    })


@login_required
@require_http_methods(['GET', 'POST'])
def product_create(request):
    if request.method == 'POST':
        Product.objects.create(
            name=request.POST.get('name', '').strip() or 'Untitled',
            description=request.POST.get('description', ''),
            status=request.POST.get('status', Product.Status.PLANNING),
            score=float(request.POST.get('score') or 0),
            notes=request.POST.get('notes', ''),
            owner=request.user,
        )
        return redirect('pipeline:kanban')
    return render(request, 'pipeline/product_form.html', {'statuses': Product.Status})


@login_required
@require_POST
def product_move(request, pk):
    new_status = request.POST.get('status')
    if new_status not in {s for s, _ in Product.Status.choices}:
        return HttpResponseBadRequest('Invalid status')
    product = get_object_or_404(Product, pk=pk)
    product.status = new_status
    product.save(update_fields=['status', 'updated_at'])
    return HttpResponse(status=204)


@login_required
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'pipeline/product_detail.html', {'product': product})
