"""overpokeapi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from rest_framework.authtoken.views import ObtainAuthToken
from .views import UserMeView, AddGroupView, RemoveGroupView, AllMyPokemonsView, MyPokemonView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/login', ObtainAuthToken.as_view()),
    path('api/group/<str:type_id>/add', AddGroupView.as_view()),
    path('api/group/<str:type_id>/remove', RemoveGroupView.as_view()),
    path('api/user/me', UserMeView.as_view()),
    path('api/pokemon', AllMyPokemonsView.as_view()),
    path('api/pokemon/<str:pokemon_id_or_name>', MyPokemonView.as_view()),

]
