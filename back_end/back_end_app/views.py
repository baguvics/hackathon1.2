from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from . import models, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from rest_framework import generics, authentication, permissions


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
