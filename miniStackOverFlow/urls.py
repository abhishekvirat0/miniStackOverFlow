"""
URL configuration for miniStackOverFlow project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.routers import DefaultRouter

from answers.views import AnswerViewSet
from notifications.views import NotificationViewSet
from questions.views import QuestionViewSet

router = DefaultRouter()
router.register(r'questions', QuestionViewSet)
router.register(r'answers', AnswerViewSet)
router.register(r'notifications', NotificationViewSet)

schema_view = get_schema_view(
   openapi.Info(
      title="Mini Stack Overflow API",
      default_version='v1',
      description="API documentation for the Mini Stack Overflow project.",
      contact=openapi.Contact(email="officialoneabhishek@gmail.com"),
      license=openapi.License(name="Abhishek"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)
urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/', include(router.urls)),
    path('api/users/', include('users.urls')),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui')
]
