import qrcode
import barcode
from barcode.writer import ImageWriter
from django.http import HttpResponse, FileResponse
from django.shortcuts import render
from django.conf import settings
import os
from io import BytesIO
from barcode import Code128


# Home page view
def home(request):
    return render(request, 'codes/home.html')

# Ensure the media directory exists
MEDIA_DIR = os.path.join(settings.BASE_DIR, 'media')
if not os.path.exists(MEDIA_DIR):
    os.makedirs(MEDIA_DIR)
from django.conf import settings

def generate_qr(request):
    download_link = None
    if request.method == "POST":
        # Get input data from the form
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        message = request.POST.get('message')

        # Combine all data into a string for the QR code
        qr_data = f"Name: {name}\nEmail: {email}\nPhone: {phone}\nAddress: {address}\nMessage: {message}"

        # Generate the QR code
        qr = qrcode.make(qr_data)

        # Create a filename based on the user's input (e.g., based on name or a unique identifier)
        qr_filename = f"qr_code_{name.replace(' ', '_')}.png"
        qr_path = os.path.join(settings.MEDIA_ROOT, qr_filename)

        # Save the QR code image
        qr.save(qr_path)

        # Provide the download link using MEDIA_URL
        download_link = f"{settings.MEDIA_URL}{qr_filename}"

    return render(request, 'codes/generate_qr.html', {'download_link': download_link})



# Barcode generation view
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

# File download view
def download_file(request, filename):
    barcode_path = os.path.join(settings.MEDIA_ROOT, filename)

    if os.path.exists(barcode_path):
        with open(barcode_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type='image/png')
            response['Content-Disposition'] = f'attachment; filename={filename}'  # This forces download
            return response
    else:
        return HttpResponse("File not found", status=404)
