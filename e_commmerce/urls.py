from django.urls import path
from .views import (
    RegisterAPIView, 
    LoginAPIView, 
    ProductListingAPIView, 
    ProductListingAllUserAPIView, 
    ProductDetailAPIVIew, 
    ProductDetailAllUserAPIVIew, 
    CartProductAddAPIView,
    CartProductViewAPIView,
    CartProductEditAPIView,
    CreateOrderAPIView,
    OrderDetailAPIView
    )

urlpatterns = [
    path('register',RegisterAPIView.as_view()),
    path('login',LoginAPIView.as_view()),

    path('product-listing',ProductListingAllUserAPIView.as_view()),
    path('product-detail/<int:id>',ProductDetailAllUserAPIVIew.as_view()),

    path('product-listing/authenticated',ProductListingAPIView.as_view()),
    path('product-detail/authenticated/<int:id>',ProductDetailAPIVIew.as_view()),

    path('cart-product-add',CartProductAddAPIView.as_view()),
    path('cart-product-view',CartProductViewAPIView.as_view()),
    path('cart-product-edit/<int:id>',CartProductEditAPIView.as_view()),

    path('order-create',CreateOrderAPIView.as_view()),
    path('order-detail/<int:id>',OrderDetailAPIView.as_view()),
]

#eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzAzMzQxMzU4LCJpYXQiOjE3MDI0NzczNTgsImp0aSI6ImY3MWFkYmI4ZWYxNjQ4YjRiNTBkYWQzZGQzODZlNDI1IiwidXNlcl9pZCI6N30.HRMOpvpfpy0lx1c_oOG72nOy1Xsnypj0Hjfs5UjAgas