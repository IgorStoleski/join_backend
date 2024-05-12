from django.urls import reverse, resolve
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.test import SimpleTestCase, Client, TestCase
from api.models import Task
from api.views import UserView, LoginView, LogoutView, TasksItemView, ContactView

class UserViewTests(TestCase):
    def setUp(self):
        # Erstellen eines Benutzers für den Login
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.welcome_url = reverse('tasks')

    def test_create_user(self):
        """
        Create a new user with the given data.
        """
        url = reverse('user-list')
        data = {
            'username': 'newuser', 
            'last_name': 'newuser_lastname', 
            'password': 'newpassword', 
            'email': 'test@mail.de'
            }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_user(self):
        """
        Get the user with the given id.
        """
        url = reverse('user-detail', kwargs={'pk': self.user.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')
        
class TestUrls(SimpleTestCase):
    def test_list_url_is_resolved(self):
        """
        Test if the URL for the list view is resolved correctly.
        """
        url = reverse('register')
        resolved_func = resolve(url).func
        self.assertEquals(resolved_func.__name__, UserView.as_view().__name__)
    
    def test_login_url_is_resolved(self):
        """
        Test if the URL for the list view is resolved correctly.
        """
        url = reverse('login')
        resolved_func = resolve(url).func
        self.assertEquals(resolved_func.__name__, LoginView.as_view().__name__)
    
    def test_logout_url_is_resolved(self):
        """
        Test if the URL for the list view is resolved correctly.
        """
        url = reverse('logout')
        resolved_func = resolve(url).func
        self.assertEquals(resolved_func.__name__, LogoutView.as_view().__name__)
    
    def test_tasks_url_is_resolved(self):
        """
        Test if the URL for the list view is resolved correctly.
        """
        url = reverse('tasks')
        resolved_func = resolve(url).func
        self.assertEquals(resolved_func.__name__, TasksItemView.as_view().__name__)
    
    def test_contact_url_is_resolved(self):
        """
        Test if the URL for the list view is resolved correctly.
        """
        url = reverse('contacts')
        resolved_func = resolve(url).func
        self.assertEquals(resolved_func.__name__, ContactView.as_view().__name__)

class TasksItemViewTests(TestCase):
    def setUp(self):
        """
        Set up the test client and create a new task.
        """
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.task = Task.objects.create(
            title = "Test Task", 
            description = "Test Description",
            due_date = "2022-12-12",
            status = "todo",
            category = "User Story",
            priority =  "low",
            assignedTo = 'Test User',
            bgcolor = '#FFFFFF',
            subtasks = 'Test Subtask',
            author=self.user 
            )
        self.url = reverse('tasks')  

    def test_get_single_task(self):
        """
        Get the task with the given id.
        """
        url = reverse('task-detail', kwargs={'pk': self.user.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_tasks(self):
        """
        Get all tasks.
        """
        url = reverse('tasks')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_valid_task(self):
        """
        Post a new task with the given data.
        """
        url = reverse('tasks')
        data = {
            'title': 'New Task', 
            'description': 'New Description',
            'due_date': "2022-12-12",
            'status': "todo",
            'category': "User Story",
            'priority':  "low",
            'assignedTo': 'Test User',
            'bgcolor': '#FFFFFF',
            'subtasks': 'Test Subtask',
            }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_put_task(self):
        """
        Update the task with the given id.
        """
        url = reverse('task-detail', kwargs={'pk': self.task.pk})
        data = {
            'title': 'New Task2', 
            'description': 'New Description2',
            'due_date': "2025-12-12",
            'status': "todo",
            'category': "User Story",
            'priority':  "low",
            'assignedTo': 'Test User',
            'bgcolor': '#FFFFFF',
            'subtasks': 'Test Subtask',
            }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_task(self):
        """
        Delete the task with the given id.
        """
        url_detail = reverse('task-detail', kwargs={'pk': self.task.pk})
        response = self.client.delete(url_detail)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        

    def test_unauthorized_access(self):
        """
        Test if the user is unauthorized to access the tasks.
        """
        self.client.credentials()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)