from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods, require_POST

from .forms import CampaignForm, ProductForm
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
    form = ProductForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            product = form.save(commit=False)
            product.owner = request.user
            product.save()
            return redirect('pipeline:product_detail', pk=product.pk)
    return render(request, 'pipeline/product_form.html', {
        'form': form,
        'title': 'New product',
        'submit_label': 'Create',
    })


@login_required
@require_http_methods(['GET', 'POST'])
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    form = ProductForm(request.POST or None, instance=product)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('pipeline:product_detail', pk=product.pk)
    return render(request, 'pipeline/product_form.html', {
        'form': form,
        'product': product,
        'title': 'Edit product',
        'submit_label': 'Save changes',
    })


@login_required
@require_http_methods(['GET', 'POST'])
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('pipeline:kanban')
    return render(request, 'confirm_delete.html', {
        'object': product,
        'object_type': 'product',
        'cancel_url': product.get_absolute_url() if hasattr(product, 'get_absolute_url') else 'pipeline:kanban',
        'cancel_href': request.META.get('HTTP_REFERER') or '/',
    })


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


@login_required
@require_http_methods(['GET', 'POST'])
def campaign_create(request, product_pk=None):
    product = get_object_or_404(Product, pk=product_pk) if product_pk else None
    form = CampaignForm(request.POST or None, product=product)
    if request.method == 'POST' and form.is_valid():
        campaign = form.save()
        return redirect('pipeline:product_detail', pk=campaign.product.pk)
    return render(request, 'pipeline/campaign_form.html', {
        'form': form,
        'product': product,
        'title': 'New campaign',
        'submit_label': 'Create campaign',
    })


@login_required
@require_http_methods(['GET', 'POST'])
def campaign_update(request, pk):
    campaign = get_object_or_404(Campaign, pk=pk)
    form = CampaignForm(request.POST or None, instance=campaign)
    if request.method == 'POST' and form.is_valid():
        campaign = form.save()
        return redirect('pipeline:product_detail', pk=campaign.product.pk)
    return render(request, 'pipeline/campaign_form.html', {
        'form': form,
        'campaign': campaign,
        'product': campaign.product,
        'title': 'Edit campaign',
        'submit_label': 'Save changes',
    })


@login_required
@require_http_methods(['GET', 'POST'])
def campaign_delete(request, pk):
    campaign = get_object_or_404(Campaign, pk=pk)
    product_pk = campaign.product.pk
    if request.method == 'POST':
        campaign.delete()
        return redirect('pipeline:product_detail', pk=product_pk)
    return render(request, 'confirm_delete.html', {
        'object': campaign,
        'object_type': 'campaign',
        'cancel_href': request.META.get('HTTP_REFERER') or f'/product/{product_pk}/',
    })
