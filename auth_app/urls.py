from django.urls import path, include
from django.contrib.auth import views as auth_views

app_name = 'auth_app'
urlpatterns = [
    path('logged_out/', auth_views.LogoutView.as_view(template_name='auth_app/logout.html')),
    path('login/', auth_views.LoginView.as_view(template_name='auth_app/login.html'), name='login'),
    path('', include('django.contrib.auth.urls')),
]
