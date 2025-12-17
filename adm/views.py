
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from accounts.forms import CustomUserCreationForm
from django.contrib.auth.forms import UserChangeForm
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from chat.models import Message
from django.contrib.auth.models import User
from contact.models import Contact
from contact.forms import ContactForm
from images.models import Image
from images.forms import ImageForm
from django.http import HttpResponse
from payments.forms import PaymentForm
from payments.models import Transaction
import csv


# Dashboard home
def dashboard(request):
    return render(request, 'adm/dashboard.html')


# users crud operation

# LIST Users
def user_list(request):
    users = User.objects.all()
    return render(request, 'adm/user_list.html', {'users': users})


# CREATE User
def user_create(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "User created successfully.")
            return redirect('adm:user_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'adm/user_form.html', {'form': form})


# EDIT User
def user_edit(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "User updated successfully.")
            return redirect('adm:user_list')
    else:
        form = UserChangeForm(instance=user)
    return render(request, 'adm/user_form.html', {'form': form})


# DELETE User
def user_delete(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.delete()
        messages.success(request, "User deleted successfully.")
        return redirect('adm:user_list')
    return render(request, 'adm/user_confirm_delete.html', {'user': user})



# chat crud operations


# Only allow superusers/admins to access
def admin_required(view_func):
    return user_passes_test(lambda u: u.is_superuser)(view_func)

@admin_required
def message_list(request):
    messages = Message.objects.all().order_by('-timestamp')
    return render(request, 'adm/message_list.html', {'messages': messages})

@admin_required
def message_create(request):
    if request.method == 'POST':
        user_id = request.POST.get('user')
        content = request.POST.get('content')
        if user_id and content:
            user = get_object_or_404(User, id=user_id)
            Message.objects.create(user=user, content=content)
            return redirect('adm_message_list')
    users = User.objects.all()
    return render(request, 'adm/message_form.html', {'users': users})

@admin_required
def message_update(request, pk):
    message = get_object_or_404(Message, pk=pk)
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            message.content = content
            message.save()
            return redirect('adm_message_list')
    return render(request, 'adm/message_form.html', {'message': message})

@admin_required
def message_delete(request, pk):
    message = get_object_or_404(Message, pk=pk)
    if request.method == 'POST':
        message.delete()
        return redirect('adm_message_list')
    return render(request, 'adm/message_confirm_delete.html', {'message': message})


# contact crud operations


def admin_required(view_func):
    return user_passes_test(lambda u: u.is_superuser)(view_func)

@admin_required
def contact_list(request):
    contacts = Contact.objects.all().order_by('-id')
    return render(request, 'adm/contact_list.html', {'contacts': contacts})

@admin_required
def contact_create(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('adm_contact_list')
    else:
        form = ContactForm()
    return render(request, 'adm/contact_form.html', {'form': form})

@admin_required
def contact_update(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    if request.method == 'POST':
        form = ContactForm(request.POST, instance=contact)
        if form.is_valid():
            form.save()
            return redirect('adm_contact_list')
    else:
        form = ContactForm(instance=contact)
    return render(request, 'adm/contact_form.html', {'form': form})

@admin_required
def contact_delete(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    if request.method == 'POST':
        contact.delete()
        return redirect('adm_contact_list')
    return render(request, 'adm/contact_confirm_delete.html', {'contact': contact})


# images crud operatrions

def admin_required(view_func):
    return user_passes_test(lambda u: u.is_superuser)(view_func)

@admin_required
def image_list(request):
    images = Image.objects.all().order_by('-uploaded_at')
    return render(request, 'adm/image_list.html', {'images': images})

@admin_required
def image_create(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('adm_image_list')
    else:
        form = ImageForm()
    return render(request, 'adm/image_form.html', {'form': form})

@admin_required
def image_update(request, pk):
    image = get_object_or_404(Image, pk=pk)
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES, instance=image)
        if form.is_valid():
            form.save()
            return redirect('adm_image_list')
    else:
        form = ImageForm(instance=image)
    return render(request, 'adm/image_form.html', {'form': form})

@admin_required
def image_delete(request, pk):
    image = get_object_or_404(Image, pk=pk)
    if request.method == 'POST':
        image.delete()
        return redirect('adm_image_list')
    return render(request, 'adm/image_confirm_delete.html', {'image': image})


# crud operations for payments

def admin_required(view_func):
    return user_passes_test(lambda u: u.is_superuser)(view_func)

@admin_required
def payment_list(request):
    payments = Transaction.objects.all().order_by('-created_at')
    return render(request, 'adm/payment_list.html', {'payments': payments})

@admin_required
def payment_create(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('adm_payment_list')
    else:
        form = PaymentForm()
    return render(request, 'adm/payment_form.html', {'form': form})

@admin_required
def payment_update(request, pk):
    payment = get_object_or_404(Transaction, pk=pk)
    if request.method == 'POST':
        form = PaymentForm(request.POST, instance=payment)
        if form.is_valid():
            form.save()
            return redirect('adm_payment_list')
    else:
        form = PaymentForm(instance=payment)
    return render(request, 'adm/payment_form.html', {'form': form})

@admin_required
def payment_delete(request, pk):
    payment = get_object_or_404(Transaction, pk=pk)
    if request.method == 'POST':
        payment.delete()
        return redirect('adm_payment_list')
    return render(request, 'adm/payment_confirm_delete.html', {'payment': payment})

@admin_required
def payment_download_csv(request):
    payments = Transaction.objects.all().order_by('-created_at')
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="payments.csv"'

    writer = csv.writer(response)
    writer.writerow(['Name', 'Phone Number', 'Amount', 'Status', 'Transaction ID', 'Created At'])

    for p in payments:
        writer.writerow([p.name, p.phone_number, p.amount, p.status, p.transaction_id, p.created_at])

    return response
