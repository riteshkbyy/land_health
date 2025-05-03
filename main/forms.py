from django import forms
from .models import HealthCard


class HealthCardForm(forms.ModelForm):
    status = forms.MultipleChoiceField(
        choices=HealthCard.PUBLISH_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    class Meta:
        model = HealthCard
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(HealthCardForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.widget.input_type == 'checkbox':
                field.widget.attrs.update({
                    'class': 'form-check-input'
                })
            else:
                field.widget.attrs.update({
                    'class': 'form-control',
                    'placeholder': field.label
                })