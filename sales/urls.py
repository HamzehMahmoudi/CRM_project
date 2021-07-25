from sales.models import Quote
from django.urls import path, include
from . import views


urlpatterns = [
    path("send_email", views.email, name="email"),
    path("quotlist", views.QuoteList.as_view(), name="quotelist"),
    path("quotdetail/<int:pk>", views.QuoteDetail.as_view(), name="qoute-detail"),
    path("create-quote/<int:pk>", views.create_quote, name="create-quote"),
    path("quote/add/<int:qid>", views.add_item, name="add-item")
]
