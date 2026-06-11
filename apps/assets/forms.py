from django import forms

from .models import Angle, Creative, Hook


class StyledFormMixin:
    def _style_fields(self):
        for field in self.fields.values():
            existing = field.widget.attrs.get('class', '')
            if not isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = f'{existing} app-input'.strip()


class AngleForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Angle
        fields = ['name', 'category', 'success_rate']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._style_fields()


class CreativeForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Creative
        fields = ['title', 'campaign', 'angle', 'file', 'media_type', 'is_winner']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._style_fields()
        self.fields['is_winner'].widget.attrs['class'] = 'h-4 w-4 rounded border-slate-300 text-indigo-600'


class HookForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Hook
        fields = ['text', 'platform', 'trigger_type', 'angle', 'performance_score']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._style_fields()
