from django.urls import path, include
from . import views


urlpatterns = [
    path("", views.Organlist.as_view(), name="organlist"),
    path("create", views.CreateOragan.as_view(), name="createorgan"),


]
