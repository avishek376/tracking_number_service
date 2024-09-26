from django.urls import path
from . import views
urlpatterns = [
    path('',views.TrackingNumberView.as_view(), name='next_tracking_number'),
]