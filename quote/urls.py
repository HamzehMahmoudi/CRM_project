from django.urls import path, include
from . import views


urlpatterns = [
    path("list", views.QuoteList.as_view(), name="quotelist"),
    path("detail/<int:pk>", views.QuoteDetail.as_view(), name="quote-detail"),
    path("create/<int:pk>", views.create_quote, name="create-quote"),
    path("item-add/<int:qid>", views.add_item, name="add-item"),
    path("item-delete/<int:pk>",
         views.delete_quote_item, name="delete-item"),
]
