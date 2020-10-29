from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf.urls import url
from django.views.static import serve
from api_yamdb import settings


urlpatterns = [
    path('admin/', admin.site.urls),    
    path('redoc/', TemplateView.as_view(template_name='redoc.html'), name='redoc'),
    path('api/v1/', include('api_yamdb._urls.api')),    
]

urlpatterns += [
   url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT, 'show_indexes': settings.DEBUG})
]
