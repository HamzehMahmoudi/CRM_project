from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.OrganizationList.as_view(), name="organlist"),
    path("create", views.CreateOrganization.as_view(), name="createorgan"),
    path("detail/<int:pk>", views.OrganizationDetail.as_view(), name="orgdetail"),
    path("edit/<int:pk>", views.OrganizationUpdate.as_view(), name="orgedit"),
    path("product/list", views.ProductList.as_view(), name="product-list"),
    path("api/v1", views.OrganizationListApi.as_view(), name="organapi"),
    path('api-auth/', include('rest_framework.urls')),



]
