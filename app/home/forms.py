from django import forms

from .models import Flock, Feed, CoupeDay


class FlockForm(forms.ModelForm):
    location = forms.CharField(max_length=64)

    class Meta:
        model = Flock
        fields = {'name', 'birds_count', 'breed', 'notes'}
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 5}),
            'location': forms.TextInput()
        }


class FeedForm(forms.ModelForm):
    class Meta:
        model = Feed
        fields = {'name', 'ingredients', 'notes'}
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 5}),
            'ingredients': forms.Textarea(attrs={'rows': 5})

        }


class CoupeDayForm(forms.ModelForm):
    class Meta:
        model = CoupeDay
        fields = {'date', 'collected_eggs', 'flock', 'notes', 'feed', 'feed_amount_kg', }
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 5}),
            'date': forms.DateInput(attrs={'type': 'date'})
        }
        help_texts = {
            'date': 'Pleas be advised that weather data is only available for last five days, '
                    'records with older dates will have weather data from date of creating'
        }

    def __init__(self, *args, **kwargs):
        author = kwargs.pop('author')
        super().__init__(*args, **kwargs)
        self.fields['flock'].queryset = Flock.objects.filter(author=author)
        self.fields['flock'].empty_label = 'No flocks, please add one'
        self.fields['feed'].queryset = Feed.objects.filter(author=author)
        self.fields['feed'].empty_label = 'No feed, please add one'
