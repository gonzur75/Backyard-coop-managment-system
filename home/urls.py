from django.urls import path

from . import views
from .views import HomeView, FlockView, FeedView, CoupeDayView

app_name = 'home'

urlpatterns = [
    path('', HomeView.as_view(), name='index'),
    path('flocks/', FlockView.as_view(), name='flocks'),
    path('feed/', FeedView.as_view(), name='feed'),
    path('frecords/', CoupeDayView.as_view(), name='records'),
    path('egg_per_day/', views.egg_chart, name='egg_chart'),
]