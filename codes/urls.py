from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from django.views.static import serve
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('generate-qr/', views.generate_qr, name='generate_qr'),
    path('generate-barcode/', views.generate_barcode, name='generate_barcode'),
    path('media/<str:filename>/', views.download_file, name='download_file'),# urls.py
    # Your existing URL patterns
    path('generate-barcode/', views.generate_barcode, name='generate_barcode'),
    # other paths
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)