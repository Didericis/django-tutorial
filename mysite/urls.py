from django.contrib import admin
from django.urls import include, path 
from django.views.generic.base import RedirectView

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include('api.urls')),
    path('auth/', include('auth_app.urls')),
    path('polls/', include('polls.urls')),
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='polls/', permanent=False), name='index')
]
