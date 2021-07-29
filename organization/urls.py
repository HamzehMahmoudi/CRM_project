from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.Organlist.as_view(), name="organlist"),
    path("create", views.CreateOragan.as_view(), name="createorgan"),
    path("detail/<int:pk>", views.OrgDetail.as_view(), name="orgdetail"),
    path("edit/<int:pk>", views.OrgUpdate.as_view(), name="orgedit"),
    path("product/list", views.ProductList.as_view(), name="product-list"),
    path("api/v1", views.OrganizationListApi.as_view(), name="organapi"),
    path('api-auth/', include('rest_framework.urls')),



]
