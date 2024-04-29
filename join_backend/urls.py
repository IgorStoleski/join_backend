"""
URL configuration for join_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from api.views import UserView
from api.views import LoginView, LogoutView, TasksItemView, ContactView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', UserView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('tasks/', TasksItemView.as_view(), name='tasks'),
    path('tasks/<int:pk>/', TasksItemView.as_view(), name='task-detail'),
    path('users/', UserView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserView.as_view(), name='user-detail'),
    path('contacts/', ContactView.as_view(), name='contacts'),
    path('contacts/<int:pk>/', ContactView.as_view(), name='contacts-detail'),
]
