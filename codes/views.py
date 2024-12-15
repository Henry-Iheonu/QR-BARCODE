import qrcode
import barcode
from barcode.writer import ImageWriter
from django.http import HttpResponse, Http404, FileResponse
from django.shortcuts import render
from django.conf import settings
import os
from barcode.errors import BarcodeError
from barcode import get_barcode_class


# Home page view
def home(request):
    return render(request, 'codes/home.html')

# Ensure the media directory exists
MEDIA_DIR = os.path.join(settings.BASE_DIR, 'media')
if not os.path.exists(MEDIA_DIR):
    os.makedirs(MEDIA_DIR)

# QR Code generation view
def generate_qr(request):
    download_link = None
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        address = request.POST['address']
        message = request.POST['message']

        data = f"Name: {name}\nEmail: {email}\nPhone: {phone}\nAddress: {address}\nMessage: {message}"
        img = qrcode.make(data)

        qr_filename = 'qr_code.png'
        img_path = os.path.join(MEDIA_DIR, qr_filename)
        img.save(img_path)

        download_link = f'/media/{qr_filename}'
    return render(request, 'codes/generate_qr.html', {'download_link': download_link})

def generate_barcode(request):
    download_link = None
    if request.method == 'POST':
        product_code = request.POST['product_code']

        # Ensure the product_code is exactly 13 digits for EAN-13 barcode
        if len(product_code) != 13:
            return render(request, 'codes/generate_barcode.html', {
                'error': 'The barcode number must be exactly 13 digits!'
            })

        # Generate barcode (EAN-13 format)
        BarcodeClass = barcode.get_barcode_class('ean13')
        generated_barcode = BarcodeClass(product_code, writer=ImageWriter())

        # Define the barcode file name and its path in the media directory
        barcode_filename = f'{product_code}_barcode.png'
        barcode_path = os.path.join(settings.MEDIA_ROOT, barcode_filename)

        # Save the barcode image to the media folder
        generated_barcode.save(barcode_path)

        # Provide a download link for the barcode image
        download_link = f'{settings.MEDIA_URL}{barcode_filename}'

    return render(request, 'codes/generate_barcode.html', {'download_link': download_link})


def download_file(request, filename):
    barcode_path = os.path.join(settings.MEDIA_ROOT, filename)

    if os.path.exists(barcode_path):
        with open(barcode_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type='image/png')
            response['Content-Disposition'] = f'attachment; filename={filename}'  # This forces download
            return response
    else:
        return HttpResponse("File not found", status=404)
