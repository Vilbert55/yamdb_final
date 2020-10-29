from django.urls import path, include
from rest_framework.routers import DefaultRouter

from titles.views import GenreListCreateDeleteView


router = DefaultRouter()


router.register('', GenreListCreateDeleteView)

urlpatterns = router.urls
