from django.urls import path
from rest_framework.routers import DefaultRouter

from user_api.views import UserViewSet, UserGeneric


router = DefaultRouter()


router.register('', UserViewSet)


urlpatterns = [
    path('me/', UserGeneric.as_view()),
]
urlpatterns += router.urls
