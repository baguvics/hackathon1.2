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
# Генерация статьи
class ArticleView(APIView):
    def post(self, request):
            temp_data = {
            'title_of_article': 'Бухгалтерия — где найти, как составить. 1C',
            'annotation':   'В данном тексте рассказывается о процессе настройки и формирования штатного расписания в программе 1С бухгалтерии.',
            'summary':  [
                            ' Для этого нужно проверить настройки зарплаты и кадрового учета, а также флаг "Кадровые документы". Затем перейти в раздел "Отчеты по кадрам" и сформировать отчет "Штатные сотрудники". Он не будет похож на штатное расписание, но поможет создать его, удалив лишнюю информацию. Таким образом, в 1С бухгалтерии можно создать штатное расписание.',
                            ' единиц, тарифную ставку и надбавки. Настройка отчета завершена."Настройка отчета о штатных сотрудниках": для того, чтобы правильно настроить отчет, нам нужно понять, какие сведения нам необходимы. Обычно штатное расписание организации утверждается на основе унифицированной формы Т3. Нам потребуется структурное подразделение, должность, количество штатных единиц, тарифная ставка и надбавки. В настройках вид формы должен быть расширенным, а вот группа И и группа ИЛИ не нужны.',
                            'Нам нужны сотрудники, табельный номер, должность, тарифная ставка, дата увольнения для уволенных и вакантных должностей, рабочий телефон. В форме штатного расписания должны быть сведения о надбавках. Для этого в настройках отчета нужно вывести их. Открываем папку работа, приказ о приеме, находим начисления, открываем наименование и размер. Передвигаем поближе, проверяем структуру, закрываем и сформировываем. Отчет более компактный, содержит информацию об окладе и надбавка',
                            'Для штатного расписания в 1С бухгалтерии нажмите на кнопку «Сохранить как» и выберите раздел, в котором должен сохраниться отчет, например, «Кадры». Затем нажмите «Сохранить». Отчет сформирован и выгружен в Excel. Если вам нужна дополнительная информация, посмотрите нашу статью «Штатное расписание в 1С бухгалтерии». Подписывайтесь на наш канал, чтобы не пропустить новые видео. Нажмите на колокольчик и получайте уведомления о новых видео. До новых встреч!'
                        ],
            'titles':   [
                            'Как создать штатное расписание в Одинэс бухгалтерии?',
                            'Настройка отчета о штатных сотрудниках',
                            'Формирование штатного расписания: настройки и сохранение',
                            'Штатное расписание в 1С бухгалтерии: простая настройка'
                        ],
            'timings':  ['00:00:00-00:01:47', '00:01:47-00:03:33', '00:03:33-00:05:39', '00:05:39-00:06:44'],
            'frames':   [['frame_308.jpg', 'frame_2341.jpg'], ['frame_6390.jpg'], 
                        ['frame_10170.jpg'], ['frame_11197.jpg']]
            }

            return Response(temp_data)


    

    