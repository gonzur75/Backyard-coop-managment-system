from django import forms

from .models import Flock, Feed, CoupeDay


class FlockForm(forms.ModelForm):
    class Meta:
        model = Flock
        fields = {'name', 'birds_count', 'breed', 'notes', 'location'}
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 5})
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

    def __init__(self, *args, **kwargs):
        author = kwargs.pop('author')
        super(CoupeDayForm, self).__init__(*args, **kwargs)
        self.fields['flock'].queryset = Flock.objects.filter(author=author)
        self.fields['flock'].empty_label = 'No flocks, please add one'
        self.fields['feed'].queryset = Feed.objects.filter(author=author)
        self.fields['feed'].empty_label = 'No feed, please add one'
