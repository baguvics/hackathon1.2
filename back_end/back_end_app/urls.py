from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view as swagger_get_shema_view
from . import views

shema_view = swagger_get_shema_view(
    openapi.Info(
        title="Posts API",
        default_version='1.0.0',
        description="API documentation of App"
    ),
    public=True,
)

urlpatterns = [
    path('api/v1/',
        include([
            path('swagger/', shema_view.with_ui('swagger', cache_timeout=0)),  # Все апишки
            path('register/', views.RegisterView.as_view(), name='register'),  # Регистрация
            path('login/', views.LoginView.as_view(), name='login'),           # Авторизация
            path('user/', views.UserProfileView.as_view(), name='user'),       # Получение данных пользователя

        ]))
]