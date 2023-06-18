from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login, authenticate
from django.contrib import messages
from django.db import models
from .models import Music

def protected_music_files(request):
    user = request.user
    email = None  
    if user.is_authenticated:
        email = user.email  
    return render(request, 'protected_music_files.html', {'email': email})

@login_required
def upload_music(request):
    if request.method == 'POST':
        file = request.FILES['file']  
        access = request.POST['access']
        allowed_emails = request.POST.getlist('allowed_emails')

        music = Music(user=request.user, file=file, access=access, allowed_emails=allowed_emails)
        music.save()
        return redirect('homepage')

    return render(request, 'upload.html')
    
@login_required
def homepage(request):
    user = request.user
    if user.is_authenticated:
        email = user.email
        music_files = Music.objects.filter(
            models.Q(access='public') |
            models.Q(user=user) |
            models.Q(allowed_emails__contains=email)
        )
    else:
        music_files = Music.objects.filter(access='public')

    return render(request, 'homepage.html', {'music_files': music_files})
