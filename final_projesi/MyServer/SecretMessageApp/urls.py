
from django.urls import path
from .views import index,showmessage,generatemessage

urlpatterns = [
    path('', index , name='index'),
    path('<uuid:messageId>/', showmessage, name='showmessage'),
    path('generate/',generatemessage, name='generatemessage')
]