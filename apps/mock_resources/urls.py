"""URL configuration for mock resources app."""
from django.urls import path
from apps.mock_resources.views import (
    ProductListView,
    ProductDetailView,
    OrderListView,
    OrderDetailView
)

app_name = 'mock_resources'

urlpatterns = [
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/<int:product_id>/', ProductDetailView.as_view(), name='product-detail'),
    path('orders/', OrderListView.as_view(), name='order-list'),
    path('orders/<int:order_id>/', OrderDetailView.as_view(), name='order-detail'),
]