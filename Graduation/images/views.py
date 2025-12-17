from django.shortcuts import render,redirect
from .forms import ImageForm
from .models import Image
import io
import zipfile
from django.http import HttpResponse

# Create your views here.
def enter_image(request):
    if request.method == 'POST':
        images = request.FILES.getlist('images')
        descriptions = request.POST.get('descriptions')
        for img in images:
            Image.objects.create(photo=img, description=descriptions)
        return redirect('all')
    else:
        form = ImageForm()
    context = {'form': form}
    return render(request, 'img/image_form.html', context)


def all(request):
    images = Image.objects.all().order_by('-uploaded_at')
    context = {'images': images}
    return render(request, 'img/all_img.html', context)




def download_all(request):
    # Create an in-memory ZIP file
    zip_buffer = io.BytesIO()
    
    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        for img in Image.objects.all():
            # Read image content
            img_path = img.photo.path
            zip_file.write(img_path, arcname=img.photo.name)  # arcname keeps the filename
            
    zip_buffer.seek(0)
    response = HttpResponse(zip_buffer, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename=all_images.zip'
    return response
