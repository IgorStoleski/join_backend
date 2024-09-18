
from django.contrib import admin
from django.urls import path
from api.views import UserView
from api.views import LoginView, LogoutView, TasksItemView, ContactView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


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
] + staticfiles_urlpatterns()
