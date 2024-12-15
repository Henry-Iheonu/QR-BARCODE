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

import os
from io import BytesIO
from django.http import FileResponse
from barcode import Code128
from barcode.writer import ImageWriter

def generate_barcode(request):
    if request.method == 'POST':
        barcode_number = request.POST['barcode_number']
        
        # Generate barcode
        barcode_class = Code128
        barcode_image = barcode_class(barcode_number, writer=ImageWriter())

        # Create an in-memory file
        buffer = BytesIO()
        barcode_image.write(buffer)

        # Return file as a downloadable response
        buffer.seek(0)
        response = FileResponse(buffer, as_attachment=True, filename=f'{barcode_number}_barcode.png')
        return response

    return render(request, 'codes/generate_barcode.html')



def download_file(request, filename):
    barcode_path = os.path.join(settings.MEDIA_ROOT, filename)

    if os.path.exists(barcode_path):
        with open(barcode_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type='image/png')
            response['Content-Disposition'] = f'attachment; filename={filename}'  # This forces download
            return response
    else:
        return HttpResponse("File not found", status=404)
