from django import forms

from .models import Campaign, Product


class StyledFormMixin:
    def _style_fields(self):
        for field in self.fields.values():
            existing = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = f'{existing} app-input'.strip()


class ProductForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'status', 'score', 'notes']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._style_fields()


class CampaignForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Campaign
        fields = ['product', 'name', 'start_date', 'end_date', 'budget', 'status']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, product=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._style_fields()
        if product is not None:
            self.fields['product'].initial = product
            self.fields['product'].widget = forms.HiddenInput()
