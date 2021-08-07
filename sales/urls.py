from django.urls import path, include
from . import views


urlpatterns = [
    path("send_email", views.email, name="email"),
    path("quotes/", include("quote.urls")),
    path("show-followup", views.show_followup, name="showfollowup"),
    path("create-followup", views.create_followup, name="create-followup"),
]
