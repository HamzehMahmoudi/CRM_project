from django.urls import path, include
from . import views


urlpatterns = [
    path("send_email", views.email, name="email"),
    path("quotes/", include("quote.urls")),
    path("add-followup/<int:orgid>", views.add_follow_up, name="add-followup"),
    path("show-followup", views.show_followup, name="showfollowuo"),
]
