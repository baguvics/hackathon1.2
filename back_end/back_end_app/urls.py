from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view as swagger_get_shema_view
from . import views

schema_view = swagger_get_shema_view(
    openapi.Info(
        title="Posts API",
        default_version='1.0.0',
        description="API documentation of App"
    ),
    public=True,
)

urlpatterns = [
    path('api/v1/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger'),  # Swagger API documentation
    path('api/v1/register/', views.RegisterView.as_view(), name='register'),                   # Регистрация
    path('api/v1/login/', views.LoginView.as_view(), name='login'),                            # Авторизация
    path('api/v1/user/', views.UserProfileView.as_view(), name='user'),                        # Получение данных пользователя
    path('api/v1/get_video_duration/<path:video_url>/', views.VideoView.as_view(), 
        name='get_video_duration'),                                                            # Получение видео
    path('api/v1/article/', views.ArticleView.as_view(), name='article'),                      # Генерация статьи

]