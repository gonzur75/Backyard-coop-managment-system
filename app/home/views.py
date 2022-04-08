import datetime
import os

import requests
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Avg
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import UpdateView, DeleteView, CreateView, ListView

from home.forms import FlockForm, FeedForm, CoupeDayForm
from home.models import Flock, Feed, CoupeDay, Weather, Location


class HomeView(LoginRequiredMixin, View):

    def get(self, request):
        flock_info = Flock.objects.filter(author=request.user).first()
        bird_laying = CoupeDay.objects.all().aggregate(Avg('collected_eggs'))
        total_eggs_year = CoupeDay.objects.all().aggregate(Avg('collected_eggs'))
        bird_laying = round((int(bird_laying['collected_eggs__avg']) / flock_info.birds_count) * 100)
        ctx = {
            'flock': flock_info,
            'bird_laying': bird_laying
        }
        return render(request, 'home/index.html', ctx)


class FlockView(LoginRequiredMixin, ListView):
    model = Flock
    template_name = 'home/flock/flock-view.html'

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset().filter(author=user)
        return queryset


class FlockCreateView(LoginRequiredMixin, CreateView):
    model = Flock
    form_class = FlockForm
    template_name = 'home/flock/create_flock_form.html'
    success_url = reverse_lazy('home:flocks')

    def form_valid(self, form):
        form.instance.author = self.request.user
        location_name = self.request.POST.get('location')
        google_geocode_key = os.environ.get('GOOGLE_GEOCODE_KEY')
        get_location_lat_lng = f'https://maps.googleapis.com/maps/api/geocode' \
                               f'/json?address={location_name}&key={google_geocode_key}'
        geo_data = requests.get(get_location_lat_lng).json()
        location_lat = geo_data['results'][0]['geometry']['location']['lat']
        location_lng = geo_data['results'][0]['geometry']['location']['lng']
        location_db = Location.objects.create(name=location_name,
                                              lon=location_lng,
                                              lat=location_lat)
        form.instance.location = location_db
        return super().form_valid(form)


class FlockUpdateView(LoginRequiredMixin, UpdateView):
    model = Flock
    form_class = FlockForm
    template_name = 'home/flock/create_flock_form.html'


class FlockDeleteView(LoginRequiredMixin, DeleteView):
    model = Flock
    success_url = reverse_lazy('home:flocks')
    template_name = "home/flock/flock_confirm_delete.html"


class FeedView(LoginRequiredMixin, ListView):
    model = Feed
    template_name = 'home/feed/feed-view.html'

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset().filter(author=user)
        return queryset


class FeedCreateView(LoginRequiredMixin, CreateView):
    model = Feed
    template_name = 'home/feed/create_feed_form.html'
    success_url = reverse_lazy('home:feed')
    form_class = FeedForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class FeedUpdateView(LoginRequiredMixin, UpdateView):
    model = Feed
    form_class = FeedForm
    template_name = 'home/feed/create_feed_form.html'


class FeedDeleteView(LoginRequiredMixin, DeleteView):
    model = Feed
    success_url = reverse_lazy('home:feed')
    template_name = 'home/feed/feed_confirm_delete.html'


class CoupeDayView(LoginRequiredMixin, ListView):
    model = CoupeDay
    template_name = 'home/record/records-view.html'
    ordering = ['-date']
    paginate_by = 5

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset().filter(author=user)
        return queryset

    # def get(self, request):
    #     # five_days_ago = datetime.date.today() - datetime.timedelta(days=5)
    #     form = CoupeDayForm()
    #     records = CoupeDay.objects.all()
    #     ctx = {
    #         'form': form,
    #         'records': records
    #     }
    #     return render(request, 'home/record/records-view.html', ctx)

    # def post(self, request):
    #     form = CoupeDayForm(request.POST)
    #     flock = request.POST['flock']
    #
    #     url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=55af43a751e5bcd92360c46edba2ec1d'
    #     location = Flock.objects.get(pk=flock).location
    #     weather_data = requests.get(url.format(location)).json()
    #
    #     temperature = round((weather_data['main']['temp'] - 32) / 2)
    #     weather_desc = weather_data['weather'][0]['description']
    #     print(temperature)
    #     print(weather_desc)
    #     weather = Weather.objects.create(av_temp=temperature, description=weather_desc)
    #     if form.is_valid():
    #         print(form.cleaned_data)
    #         data = form.cleaned_data
    #         CoupeDay.objects.create(
    #             date=data['date'],
    #             collected_eggs=data['collected_eggs'],
    #             flock=data['flock'],
    #             notes=data['notes'],
    #             weather=weather,
    #             feed=data['feed'],
    #             feed_amount_kg=data['feed_amount_kg']
    #         )
    #         return self.get(request)
    #     else:
    #         return HttpResponse('Record for this day already exist, you can only modify it')


def egg_chart(request):
    labels = []
    data = []
    data_temp = []
    data_layers = []
    queryset = CoupeDay.objects.all().order_by('-date').values('date', 'collected_eggs', 'weather', 'flock')

    for entry in queryset:
        labels.append(entry['date'])
        data.append(entry['collected_eggs'])
        data_temp.append(Weather.objects.get(pk=entry['weather']).av_temp)
        data_layers.append(Flock.objects.get(pk=entry['flock']).birds_count)
    print(data_layers)
    return JsonResponse(data={
        'labels': labels,
        'data': data,
        'data_temp': data_temp,
        'data_layers': data_layers,

    })


def more_than_five_days(time):
    delta = datetime.timedelta(days=5)
    time_now = datetime.date.today()
    return time < time_now - delta


class RecordCreateView(LoginRequiredMixin, CreateView):
    model = CoupeDay
    template_name = 'home/record/create_record_form.html'
    form_class = CoupeDayForm
    success_url = reverse_lazy('home:records')

    def get_form_kwargs(self):
        kwargs = super(RecordCreateView, self).get_form_kwargs()
        kwargs['author'] = self.request.user
        return kwargs


    def form_valid(self, form):
        flock = form.instance.flock
        if more_than_five_days(form.instance.date):
            time = datetime.datetime.today().strftime('%s')
        else:
            time = form.instance.date.strftime('%s')
        location = Flock.objects.get(pk=flock.id).location
        lat = location.lat
        lon = location.lon
        openweather_api_key = os.environ.get('OPEN_WEATHER_API_KEY')
        url = 'https://api.openweathermap.org/data/2.5/onecall' \
              '/timemachine?lat={}&lon={}&dt={}&units=metric&appid={}'
        weather_data = requests.get(url.format(lat, lon, time, openweather_api_key)).json()
        print(weather_data)
        temperature = sum([int(record['temp']) for record in weather_data['hourly']]) / len(weather_data['hourly'])
        temp_check = [int(record['temp']) for record in weather_data['hourly']]
        print(temperature)
        print(temp_check)
        weather_desc = weather_data['hourly'][0]['weather'][0]['description']
        weather = Weather.objects.create(av_temp=temperature, description=weather_desc)
        form.instance.weather = weather
        form.instance.author = self.request.user
        return super().form_valid(form)


class RecordUpdateView(LoginRequiredMixin, UpdateView):
    model = CoupeDay
    form_class = CoupeDayForm
    template_name = 'home/record/create_record_form.html'

    def get_form_kwargs(self):
        kwargs = super(RecordUpdateView, self).get_form_kwargs()
        print(kwargs)
        kwargs['author'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class RecordDeleteView(LoginRequiredMixin, DeleteView):
    model = CoupeDay
    success_url = reverse_lazy('home:records')
    template_name = "home/record/record_confirm_delete.html"
