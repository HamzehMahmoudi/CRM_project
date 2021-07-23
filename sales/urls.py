from django.urls import path, include
from . import views


urlpatterns = [
    path("send_email", views.email, name="email"),
    path("quotlist", views.QuoteList.as_view(), name="qoutelist"),
    path("quotdetail/<int:pk>", views.QuoteDetail.as_view(), name="qoute-detail"),

]
