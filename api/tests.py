from django.urls import reverse, resolve
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.test import SimpleTestCase, Client, TestCase
from api.views import UserView, LoginView, LogoutView, TasksItemView, ContactView

class UserViewTests(TestCase):
    def setUp(self):
        # Erstellen eines Benutzers für den Login
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.welcome_url = reverse('tasks')

    def test_create_user(self):
        """
        Stellen Sie sicher, dass wir einen neuen Benutzer erstellen können.
        """
        url = reverse('user-list')
        data = {'username': 'newuser', 'password': 'newpassword', 'email': 'test@mail.de'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_user(self):
        """
        Testet das Abrufen eines Benutzerprofils.
        """
        url = reverse('user-detail', kwargs={'pk': self.user.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')
        
class TestUrls(SimpleTestCase):
    def test_list_url_is_resolved(self):
        url = reverse('register')
        resolved_func = resolve(url).func
        self.assertEquals(resolved_func.__name__, UserView.as_view().__name__)
    
    def test_login_url_is_resolved(self):
        url = reverse('login')
        resolved_func = resolve(url).func
        self.assertEquals(resolved_func.__name__, LoginView.as_view().__name__)
    
    def test_logout_url_is_resolved(self):
        url = reverse('logout')
        resolved_func = resolve(url).func
        self.assertEquals(resolved_func.__name__, LogoutView.as_view().__name__)
    
    def test_tasks_url_is_resolved(self):
        url = reverse('tasks')
        resolved_func = resolve(url).func
        self.assertEquals(resolved_func.__name__, TasksItemView.as_view().__name__)
    
    def test_contact_url_is_resolved(self):
        url = reverse('contact')
        resolved_func = resolve(url).func
        self.assertEquals(resolved_func.__name__, ContactView.as_view().__name__)
