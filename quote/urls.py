from django.urls import path, include
from . import views


urlpatterns = [
    path("quote-list", views.QuoteList.as_view(), name="quotelist"),
    path("quote-detail/<int:pk>", views.QuoteDetail.as_view(), name="quote-detail"),
    path("quote-create/<int:pk>", views.create_quote, name="create-quote"),
    path("quote-item-add/<int:qid>", views.add_item, name="add-item"),
    path("quote-item-delete/<int:pk>",
         views.delete_quote_item, name="delete-item"),
]
