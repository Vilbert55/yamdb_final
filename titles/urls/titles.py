from django.urls import path, include
from rest_framework.routers import DefaultRouter

from titles.views import TitleViewSet, CommentViewSet, ReviewViewSet


router = DefaultRouter()


router.register('', TitleViewSet)
router.register(r'(?P<title_id>\d+)/reviews', ReviewViewSet)
router.register(r'(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments', CommentViewSet)

urlpatterns = router.urls
