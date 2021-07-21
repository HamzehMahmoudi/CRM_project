from django.urls import path, include
from . import views


urlpatterns = [
    path("", views.Organlist.as_view(), name="organlist"),
    path("creat", views.CreateOragan.as_view(), name="creatorgan"),


]
