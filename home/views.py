from django.shortcuts import render, redirect
from django.views import View

from home.forms import FlockForm
from home.models import Flock


class HomeView(View):
    def get(self, request):
        return render(request, 'home/index.html')


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





