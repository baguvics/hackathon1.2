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
        data = json.loads(request.body)
        video_url = data.get('video_url')
        power = int(data.get('power'))
        add_time = bool(data.get('addTime', False))
        start_time = int(data.get('startTime'))
        end_time = int(data.get('endTime'))


        # ssl._create_default_https_context = ssl._create_unverified_context

        # youtube_video_content = YouTube(video_url)
        # youtube_video_content.title = str(strftime("%a%d%b%Y%H%M%S", gmtime()))
        # title = youtube_video_content.title

        # audio_streams = youtube_video_content.streams.filter(only_audio=True)
        # audio_stream = audio_streams[0]
        # audio_stream.download("youtube")
        # YOUR_FILE = "youtube/{}.mp4".format(title)

        # probe = ffmpeg.probe(YOUR_FILE)
        # time = float(probe['streams'][0]['duration']) // 2

        # model = whisper.load_model("tiny")

        # result = model.transcribe("youtube/{}.mp4".format(title), verbose=True, fp16=False)


        # text = "summarize into 1500 words next text from video." + result['text'][:500]

        # summary = openai.Completion.create(
        #     model="text-davinci-003",
        #     prompt=text,
        #     max_tokens=2000,
        #     temperature=0.3
        # )

        # summary_text = summary['choices'][0]['text']

        # response_data = {
        #     'summary': summary_text,
        #     # Другие данные статьи
        # }
        return Response(str(data))
    

class Musor(APIView):
    def post(self, request):
        data = json.loads(request.body)
        value1 = int(data.get('value1'))
        value2 = int(data.get('value2'))
        return Response(str(value1 + value2))

    