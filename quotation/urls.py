
from django.contrib import admin
from django.urls import path, include
from quotation import views

urlpatterns = [
    path('', views.index, name='index'),  # type: ignore
    path('cart_box', views.cart_box, name='cart_box'),
    path('quotation_list', views.quotation_list, name='quotation_list'),
    path('quotation_labor', views.quotation_labor, name='quotation_labor'),
]
