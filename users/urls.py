from django.shortcuts import render
from django.urls import path, include
from django.views import View

from . import views
from .views import RegisterView


class LandingPageView(View):
    def get(self, request):
        return render(request, 'users/users/landing-page.html')


urlpatterns = [
    path('landing/', LandingPageView.as_view(), name='landing'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', RegisterView.as_view(), name='register'),


]

