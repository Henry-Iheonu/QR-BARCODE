from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Home page
    path('', views.home, name='home'),
    path('generate_qr/', views.generate_qr, name='generate_qr'),
    path('generate-barcode/', views.generate_barcode, name='generate_barcode'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)