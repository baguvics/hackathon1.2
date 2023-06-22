import re

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
        data = json.loads(request.body)
        video_url = data.get('video_url')
        power = int(data.get('power'))
        add_time = bool(data.get('addTime', False))
        start_time = int(data.get('startTime'))
        end_time = int(data.get('endTime'))

        ssl._create_default_https_context = ssl._create_unverified_context

        youtube_video_content = YouTube("https://www.youtube.com/watch?v=gfUlCnMrZbw")
        youtube_video_content.title = str(strftime("%a%d%b%Y%H%M%S", gmtime()))
        title = youtube_video_content.title

        high_res_streams = youtube_video_content.streams
        print(high_res_streams)
        high_res_stream = high_res_streams[1]
        high_res_stream.download("youtube")
        YOUR_FILE = "youtube/{}.mp4".format(title)

        # probe = ffmpeg.probe(YOUR_FILE)
        # time = float(probe['streams'][0]['duration']) // 2
        # width = probe['streams'][0]['width']

        model = whisper.load_model("small")

        result = model.transcribe("youtube/{}.mp4".format(title), verbose=True, fp16=False, language="russian")
        print(result["text"])

        for segment in result["segments"]:
            print("{}:{}".format(segment["start"] // 60, int(segment["start"]) & 60) + "  " + segment["text"])

        text_from_video = result["text"]
        chunk_size = 1500

        sentences = re.findall(r'[^.!?]+[.!?]', text_from_video)
        chunks = []

        current_chunk = ''
        for sentence in sentences:
            if len(current_chunk) + len(sentence) <= chunk_size:
                current_chunk += sentence
            else:
                chunks.append(current_chunk)
                current_chunk = sentence

        # Добавляем последний кусок текста
        if current_chunk:
            chunks.append(current_chunk)

        chunks_timings = []
        # Находим тайминги для каждого чанка

        i = 0
        for chunk in chunks:
            i += 1
            for segment in result["segments"]:
                if segment["text"][:7] == chunk[:7]:
                    chunks_timings.append(segment["start"])
                    print("chunk number ", i, " timing: ", segment["start"])

        summary_text = []
        openai.api_key = "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"
        prompt = "напиши абзац {} по следующему тексту из видео."
        chunk_id = 0
        for paragraph in chunks:
            chunk_id += 1
            text = prompt.format(chunk_id) + paragraph
            summary = openai.Completion.create(
                model="text-davinci-003",
                prompt=text,
                max_tokens=2000,
                temperature=0.3
            )
            summary_text.append({"paragraph {}".format(chunk_id): summary['choices'][0]['text']})
            print(summary['choices'][0]['text'])
        print(summary_text)

        response_data = {
            'summary': summary_text,
            'timings': chunks_timings,
            # Другие данные статьи
        }
        return Response(str(response_data))
    

    