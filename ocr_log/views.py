from django.shortcuts import render

# Create your views here.

def user(request):
    return render(request, "ocr_log/user_join.html")

def room(request, room_name):
    return render(request, "ocr_log/room.html", {"room_name": room_name})