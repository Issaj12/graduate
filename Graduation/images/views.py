from django.shortcuts import render,redirect
from .forms import ImageForm
from .models import Image

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
