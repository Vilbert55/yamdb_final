from rest_framework.routers import DefaultRouter

from titles.views import CategoryListCreateDeleteView


router = DefaultRouter()


router.register('', CategoryListCreateDeleteView)

urlpatterns = router.urls
