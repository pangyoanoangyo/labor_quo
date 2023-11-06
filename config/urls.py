
from django.contrib import admin
from django.urls import path, include
from quotation import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('quotation.urls')),
]
