from django.urls import path
from . import views

urlpatterns = [
    # Home page
    path('', views.home, name='home'),

    # QR code generation
    path('generate-qr/', views.generate_qr, name='generate_qr'),

    # Barcode generation and download
    path('generate-barcode/', views.generate_barcode, name='generate_barcode'),
]
