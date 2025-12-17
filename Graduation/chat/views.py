# message/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Message

@login_required
def chat_view(request):
    if request.method == "POST":
        message = request.POST.get("message")
        if message:
            Message.objects.create(user=request.user, content=message)
        return redirect("chat")  # Python handles sending message
    
    # Python fetches last 50 messages
    messages = Message.objects.order_by('-timestamp')[:50]
    return render(request, "chat/chat.html", {"messages": reversed(messages)})

def chat_link(request):
    return render(request, 'chat/chat_link.html')