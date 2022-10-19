from django.contrib.auth.models import User
from django.urls import path
from web import views
from web.views import home, entreprise, Deconnexion, logIn


urlpatterns = [
        path('', home, name="home"),
        path('register', views.register, name='register'),
        path('login', views.logIn, name='login'),
        path('activate/<uidb64>/<token>', views.activate, name="activate"),
        path('deconnexion', Deconnexion, name="deconnexion"), ]
