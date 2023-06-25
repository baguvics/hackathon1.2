import re
from .speech_recognition import create_article
from django.contrib.auth import get_user_model
from django.conf import settings
from . import models, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from rest_framework import generics, authentication, permissions
from pytube import YouTube
from urllib.parse import unquote # для декодирования URL-адреса внутри представления VideoView
import ssl
import whisper
import openai
import ffmpeg
from time import gmtime, strftime
import json
from django.core.files.storage import default_storage
from .speech_recognition import create_article


ssl._create_default_https_context = ssl._create_unverified_context

# Регистрация пользователя
User = get_user_model()
class RegisterView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        first_name = request.data.get('first_name')
        email = request.data.get('email')

        if username and password and first_name and email:
            # Проверка, существует ли пользователь с указанной почтой
            existing_user = User.objects.filter(email=email).first()
            if existing_user:
                return Response({'error': 'User with this email already exists.'})

            user = User.objects.create_user(username=username, password=password, first_name=first_name, email=email)
            return Response({'success': 'User registered successfully.', 'id': user.id})
        else:
            return Response({'error': 'Invalid username, password, first name, or email'})


# Авторизация пользователей
class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return Response({'success': 'User logged in successfully.', 'id': user.id})
        else:
            return Response({'error': 'Invalid username or password.'})
        

# Получения данных пользователя
class UserProfileView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = serializer.UserSerializer(request.user)
        return Response(serializer.data)
    

# Получение видео
class VideoView(APIView):
    def post(self, request, video_url):
        video_url = unquote(video_url)
        video = YouTube(video_url)
        duration = video.length
        return Response({'duration': duration})
    

# Генерация статьи

class ArticleView(APIView):
    def post(self, request):
        video_url = request.POST.get('videoUrl')
        power = int(request.POST.get('power'))
        add_time = request.POST.get('addTime', False)
        start_time = request.POST.get('startTime')
        end_time = request.POST.get('endTime')
        video_file = request.FILES.get('videoFile')
        video_title = video_file.name
        article_size = request.POST.get('article_size')
        print (video_url, power )

        file_path = f'back_end_app/back_end/user/{video_title}'
        with default_storage.open(file_path, 'wb+') as destination:
            for chunk in video_file.chunks():
                destination.write(chunk)
            print(f"saved at {destination}")


        response_data = create_article(video_url=video_url, power=power, start_time=start_time,
                                       end_time=end_time, add_time=add_time, video_file=video_file, article_size=0)
        
        return Response(response_data)


    

    