from django.shortcuts import render,redirect
from django.contrib import messages
from .forms import ContactForm
from django.core.mail import send_mail
from django.conf import settings
# Create your views here.



def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_instance = form.save()

            # Send email to admin
            send_mail(
                subject=f"New Contact Message from {contact_instance.name}",
                message=f"""
                            Name: {contact_instance.name}
                            Contact: {contact_instance.contact}
                            Email: {contact_instance.email}
                            Message: {contact_instance.message}
                            """,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.DEFAULT_FROM_EMAIL],  # Admin email
                fail_silently=False,
            )

            messages.success(request, 'Thank you! Your message has been sent.')
            return redirect('contact')  # or wherever you want
    else:
        form = ContactForm()
    context = {'form': form}
    return render(request, 'contact/contact.html', context)




