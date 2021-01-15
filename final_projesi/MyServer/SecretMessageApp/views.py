from django.shortcuts import render, get_object_or_404
from django.http import Http404,HttpResponse
from .models import SecretMessage
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime

# Create your views here.
@csrf_exempt
def index(request):
    return render(request,'index.html')
@csrf_exempt
def showmessage(request, messageId):
    try:
        message = get_object_or_404(SecretMessage, pk=messageId)
    except SecretMessage.DoesNotExist:
        raise Http404("Broken Link No Such Message")
    if message.IsRead:
        message.MessageContent = ''
        return render(request, 'readmessage.html', {'message': message})
    else:
        message.IsRead = True
        message.ReadingTime = datetime.now()
        message.save()
        return render(request, 'message.html', {'message': message})

@csrf_exempt
def generatemessage(request):
    if request.method == 'POST':
        content = request.POST['message']
        seconds = request.POST['seconds']

        message = SecretMessage.objects.create(MessageContent=content,ExpirationSec= seconds)
        url = request.build_absolute_uri('/'+str(message.Id))

        return HttpResponse(json.dumps({'url': url}), content_type="application/json")