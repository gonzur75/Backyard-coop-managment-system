import requests
from django.db.models import Avg
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import UpdateView, DeleteView

from home.forms import FlockForm, FeedForm, CoupeDayForm
from home.models import Flock, Feed, CoupeDay, Weather


class HomeView(View):

    def get(self, request):
        flock_info = Flock.objects.get(pk=1)
        bird_laying = CoupeDay.objects.all().aggregate(Avg('collected_eggs'))
        total_eggs_year = CoupeDay.objects.all().aggregate(Avg('collected_eggs'))
        bird_laying = round((int(bird_laying['collected_eggs__avg']) / flock_info.birds_count) * 100)
        ctx = {
            'flock': flock_info,
            'bird_laying': bird_laying
        }
        return render(request, 'home/index.html', ctx)


class FlockView(View):
    def get(self, request):
        form = FlockForm()
        flock_list = Flock.objects.all()
        ctx = {
            'form': form,
            'flock_list': flock_list
        }
        return render(request, 'home/flock-view.html', ctx)

    def post(self, request):
        form = FlockForm(request.POST)
        if form.is_valid():
            form.save()
            return self.get(request)


class FlockUpdateView(UpdateView):
    model = Flock
    fields = ['name', 'birds_count', 'breed', 'notes', 'location']
    template_name = 'home/flock-view.html'


class FlockDeleteView(DeleteView):
    model = Flock
    success_url = reverse_lazy('home:flocks')


class FeedView(View):
    def get(self, request):
        form = FeedForm()
        feed_list = Feed.objects.all
        ctx = {
            'form': form,
            'feed_list': feed_list
        }
        return render(request, 'home/feed-view.html', ctx)

    def post(self, request):
        form = FeedForm(request.POST)
        if form.is_valid():
            form.save()
            return self.get(request)


class FeedUpdateView(UpdateView):
    model = Feed
    fields = ['name', 'notes', 'ingredients']
    template_name = 'home/feed-view.html'


class FeedDeleteView(DeleteView):
    model = Feed
    success_url = reverse_lazy('home:feed')


class CoupeDayView(View):
    def get(self, request):
        # five_days_ago = datetime.date.today() - datetime.timedelta(days=5)
        form = CoupeDayForm()
        records = CoupeDay.objects.all()[:5]
        ctx = {
            'form': form,
            'records': records
        }
        return render(request, 'home/records-view.html', ctx)

    def post(self, request):
        form = CoupeDayForm(request.POST)
        flock = request.POST['flock']

        url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=55af43a751e5bcd92360c46edba2ec1d'
        location = Flock.objects.get(pk=flock).location
        weather_data = requests.get(url.format(location)).json()

        temperature = round((weather_data['main']['temp'] - 32) / 2)
        weather_desc = weather_data['weather'][0]['description']
        print(temperature)
        print(weather_desc)
        weather = Weather.objects.create(av_temp=temperature, description=weather_desc)
        if form.is_valid():
            print(form.cleaned_data)
            data = form.cleaned_data
            CoupeDay.objects.create(
                date=data['date'],
                collected_eggs=data['collected_eggs'],
                flock=data['flock'],
                notes=data['notes'],
                weather=weather,
                feed=data['feed'],
                feed_amount_kg=data['feed_amount_kg']
            )
            return self.get(request)
        else:
            return HttpResponse('Record for this day already exist, you can only modify it')


def egg_chart(request):
    labels = []
    data = []

    queryset = CoupeDay.objects.values('date', 'collected_eggs')
    for entry in queryset:
        labels.append(entry['date'])
        data.append(entry['collected_eggs'])

    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })
