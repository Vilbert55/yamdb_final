from django.urls import path, include


urlpatterns = [
    path('titles/', include('titles.urls.titles')),
    path('genres/', include('titles.urls.genres')),
    path('categories/', include('titles.urls.categories')),
    path('users/', include('user_api.urls.users')),
    path('auth/', include('user_api.urls.auth')),
]
