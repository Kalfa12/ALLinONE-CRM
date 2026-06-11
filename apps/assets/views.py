from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from .forms import AngleForm, CreativeForm, HookForm
from .models import Angle, Creative, Hook


@login_required
def index(request):
    return render(request, 'assets/index.html', {
        'angles': Angle.objects.all(),
        'creatives': Creative.objects.select_related('angle', 'campaign')[:50],
        'hooks': Hook.objects.select_related('angle')[:50],
    })


@login_required
@require_http_methods(['GET', 'POST'])
def angle_create(request):
    return save_asset_form(request, AngleForm, 'New angle', 'Create angle', 'angle')


@login_required
@require_http_methods(['GET', 'POST'])
def angle_update(request, pk):
    angle = get_object_or_404(Angle, pk=pk)
    return save_asset_form(request, AngleForm, 'Edit angle', 'Save changes', 'angle', angle)


@login_required
@require_http_methods(['GET', 'POST'])
def angle_delete(request, pk):
    return delete_asset(request, get_object_or_404(Angle, pk=pk), 'angle')


@login_required
@require_http_methods(['GET', 'POST'])
def creative_create(request):
    return save_asset_form(request, CreativeForm, 'New creative', 'Create creative', 'creative', files=True)


@login_required
@require_http_methods(['GET', 'POST'])
def creative_update(request, pk):
    creative = get_object_or_404(Creative, pk=pk)
    return save_asset_form(request, CreativeForm, 'Edit creative', 'Save changes', 'creative', creative, files=True)


@login_required
@require_http_methods(['GET', 'POST'])
def creative_delete(request, pk):
    return delete_asset(request, get_object_or_404(Creative, pk=pk), 'creative')


@login_required
@require_http_methods(['GET', 'POST'])
def hook_create(request):
    return save_asset_form(request, HookForm, 'New hook', 'Create hook', 'hook')


@login_required
@require_http_methods(['GET', 'POST'])
def hook_update(request, pk):
    hook = get_object_or_404(Hook, pk=pk)
    return save_asset_form(request, HookForm, 'Edit hook', 'Save changes', 'hook', hook)


@login_required
@require_http_methods(['GET', 'POST'])
def hook_delete(request, pk):
    return delete_asset(request, get_object_or_404(Hook, pk=pk), 'hook')


def save_asset_form(request, form_class, title, submit_label, asset_type, instance=None, files=False):
    data = request.POST or None
    file_data = request.FILES if files else None
    form = form_class(data, file_data, instance=instance)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('assets:index')
    return render(request, 'assets/form.html', {
        'form': form,
        'title': title,
        'submit_label': submit_label,
        'asset_type': asset_type,
        'object': instance,
    })


def delete_asset(request, obj, asset_type):
    if request.method == 'POST':
        obj.delete()
        return redirect('assets:index')
    return render(request, 'confirm_delete.html', {
        'object': obj,
        'object_type': asset_type,
        'cancel_href': '/assets/',
    })
