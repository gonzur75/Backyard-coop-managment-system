from django import forms

from.models import Flock


class FlockForm(forms.ModelForm):
    class Meta:
        model = Flock
        fields = {'name', 'birds_count', 'breed', 'notes'}
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 5})
        }
