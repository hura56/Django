from django.urls import path
from . import views

urlpatterns = [
    path('add_favourite_event/<int:event_id>/', views.add_favourite_event),
    path('list_favourite_events', views.list_favourite_events),
    path('remove_favourite_event/<int:event_id>/', views.remove_favourite_event),
]
