from django.urls import path

from .views import HomeView, FlockView

app_name = 'home'

urlpatterns = [
    path('', HomeView.as_view(), name='index'),
    path('flocks/', FlockView.as_view(), name='flocks'),
]