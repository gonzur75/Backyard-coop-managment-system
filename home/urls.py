from django.urls import path

from . import views
from .views import HomeView, FlockView, FeedView, CoupeDayView, FlockUpdateView, FlockDeleteView, FeedUpdateView, \
    FeedDeleteView, FeedCreateView, FlockCreateView, RecordCreateView, RecordUpdateView, RecordDeleteView

app_name = 'home'

urlpatterns = [
    path('', HomeView.as_view(), name='index'),

    path('feed/', FeedView.as_view(), name='feed'),
    path('feed/create/', FeedCreateView.as_view(), name='feed-create'),
    path('feed/<int:pk>/update/', FeedUpdateView.as_view(), name='feed-update'),
    path('feed/<int:pk>/delete/', FeedDeleteView.as_view(), name='feed-delete'),

    path('records/', CoupeDayView.as_view(), name='records'),
    path('record/create/', RecordCreateView.as_view(), name='record-create'),
    path('record/<int:pk>/update/', RecordUpdateView.as_view(), name='record-update'),
    path('record/<int:pk>/delete/', RecordDeleteView.as_view(), name='record-delete'),

    path('egg_per_day/', views.egg_chart, name='egg_chart'),

    path('flocks/', FlockView.as_view(), name='flocks'),
    path('flocks/create/', FlockCreateView.as_view(), name='flocks-create'),
    path('flocks/<int:pk>/update/', FlockUpdateView.as_view(), name='flock-update'),
    path('flocks/<int:pk>/delete/', FlockDeleteView.as_view(), name='flock-delete'),
]