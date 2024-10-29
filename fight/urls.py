from django.urls import path

from . import views
from .views import FightListView

urlpatterns = [
    path('rankings/', views.ranking_view),
    path('fights/', FightListView.as_view(), name='fight_list'),
    path('add_comment/<int:fight_id>/<str:content>/', views.add_comment),
    path('get_comments/<int:fight_id>/', views.get_comments),
    path('delete_comment/<int:comment_id>/', views.delete_comment),
    path('add_favourite_fighter/<int:fighter_id>/', views.add_favourite_fighter),
    path('list_favourite_fighters/', views.list_favourite_fighters),
    path('make_predictions/<int:fight_id>/<int:winner_prediction_id>/', views.make_prediction),
    path('show_predictions/<int:fight_id>/', views.prediction_percentage),
    path('remove_favourite_fighter/<int:fighter_id>/', views.remove_favourite_fighter),
]
