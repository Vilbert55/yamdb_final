from django.urls import path

from user_api.views import EmailVIew, token_view


urlpatterns = [
    path('token/', token_view),
    path('email/', EmailVIew.as_view()),
]
