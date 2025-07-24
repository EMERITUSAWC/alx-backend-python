from django.urls import path
from django.http import HttpResponse

def messages_view(request):
    return HttpResponse("Chat Messages Endpoint")

urlpatterns = [
    path('messages/', messages_view, name='messages'),
]