from django.urls import path

from products.views import BrandDetailView
from products.views import BrandListView
from products.views import ProductDetailView
from products.views import ProductListView

urlpatterns = [
    path('products/', ProductListView.as_view(), name='products'),
    path('products/<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('brands/', BrandListView.as_view(), name='brands'),
    path('brands/<slug:slug>/', BrandDetailView.as_view(), name='brand_detail'),
]
