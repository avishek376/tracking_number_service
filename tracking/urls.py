from django.urls import path
from . import views
urlpatterns = [
    path('',views.next_tracking_number, name='next_tracking_number'),
]