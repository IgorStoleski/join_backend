from django.urls import reverse, resolve
from rest_framework import status
from rest_framework.test import APIClient, force_authenticate
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.test import SimpleTestCase, Client, TestCase, RequestFactory
from api.models import Task, Contact, Subtask
from api.views import UserView, LoginView, LogoutView, TasksItemView, ContactView
from api.serializers import SubtaskSerializer
from django.contrib.sessions.middleware import SessionMiddleware

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
        
class LoginViewTest(TestCase):
    def setUp(self):
        """
        Set up test case by creating a test user.
        """
        self.client = APIClient()
        self.url = reverse('login')
        self.test_user = User.objects.create_user(username='testuser', password='testpassword', email='testuser@example.com')
        
    def test_login_success(self):
        """
        Test successful login with correct credentials.
        """
        response = self.client.post(self.url, {'email': 'testuser@example.com', 'password': 'testpassword'}, format='json')
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.data)
        self.assertEqual(response.data['email'], 'testuser@example.com')
        self.assertEqual(response.data['user_id'], self.test_user.pk)
        
    def test_login_failure(self):
        """
        Test login failure with incorrect credentials.
        """
        response = self.client.post(self.url, {'email': 'testuser@example.com', 'password': 'wrongpassword'}, format='json')
        
        self.assertEqual(response.status_code, 400)
        self.assertNotIn('token', response.data)
        self.assertIn('non_field_errors', response.data)

    def test_login_nonexistent_user(self):
        """
        Test login failure with a non-existent user.
        """
        response = self.client.post(self.url, {'email': 'nonexistent@example.com', 'password': 'somepassword'}, format='json')
        
        self.assertEqual(response.status_code, 400)
        self.assertNotIn('token', response.data)
        self.assertIn('non_field_errors', response.data)
        
class LogoutViewTest(TestCase):
    def setUp(self):
        """
        Set up test case by creating a test user.
        """
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.factory = RequestFactory()
        self.view = LogoutView.as_view()
        self.logout_url = reverse('logout')
        self.client = APIClient()

    def _add_session_to_request(self, request):
        """
        Add session to the request.
        """
        middleware = SessionMiddleware(lambda req: None)
        middleware.process_request(request)
        request.session.save()

    def test_logout(self):
        """
        Test if the user is logged out successfully.
        """
        request = self.factory.post(self.logout_url)
        self._add_session_to_request(request)

        force_authenticate(request, user=self.user)
        response = self.view(request)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.client.logout()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
class ContactViewTests(TestCase):
    def setUp(self):
        """
        Set up the test client and create a new contact.
        """
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.contact_list_url = reverse('contacts')
        self.contact_detail_url = lambda pk: reverse('contacts-detail', args=[pk])
        self.contact_data = {
            "name": "John",
            "surname": "Doe",
            "email": "john.doe@example.com",
            "telefon": "1234567890",
            "bgcolor": "#FF0000"
        }
        self.contact = Contact.objects.create(
            name = "Jane", 
            surname = "Doe",
            email = "jane.doe@example.com", 
            telefon = "0987654321",
            bgcolor = "#00FF00"
            )

    def test_create_contact(self):
        """
        Test creating a new contact with the given data.
        """
        response = self.client.post(self.contact_list_url, self.contact_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], self.contact_data['name'])
        self.assertEqual(response.data['email'], self.contact_data['email'])
        self.assertEqual(response.data['telefon'], self.contact_data['telefon'])

    def test_get_contact_list(self):
        """
        Test getting a list of all contacts.
        """
        response = self.client.get(self.contact_list_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_contact_detail(self):
        """
        Test getting the contact with the given id.
        """
        response = self.client.get(self.contact_detail_url(self.contact.pk), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.contact.name)
        self.assertEqual(response.data['email'], self.contact.email)
        self.assertEqual(response.data['telefon'], self.contact.telefon)

    def test_update_contact(self):
        """
        Test updating the contact with the given id.
        """
        updated_data = {
            "name": "Jane",
            "surname": "Smith",
            "email": "jane.smith@example.com",
            "telefon": "1112223333",
            "bgcolor": "#0000FF"
        }
        response = self.client.put(self.contact_detail_url(self.contact.pk), updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], updated_data['name'])
        self.assertEqual(response.data['surname'], updated_data['surname'])
        self.assertEqual(response.data['email'], updated_data['email'])
        self.assertEqual(response.data['telefon'], updated_data['telefon'])

    def test_delete_contact(self):
        """
        Test deleting the contact with the given id.
        """
        response = self.client.delete(self.contact_detail_url(self.contact.pk), format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Contact.objects.filter(pk=self.contact.pk).exists())

    def test_create_contact_invalid_data(self):
        """
        Test creating a new contact with invalid data.
        """
        invalid_data = {
            "name": "",
            "surname": "Doesn't matter",
            "email": "not-an-email",
            "telefon": "not-a-phone-number",
            "bgcolor": "not-a-color"
        }
        response = self.client.post(self.contact_list_url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_contact_invalid_data(self):
        """
        Test updating the contact with invalid data.
        """
        invalid_data = {
            "name": "",
            "surname": "Doesn't matter",
            "email": "not-an-email",
            "telefon": "not-a-phone-number",
            "bgcolor": "not-a-color"
        }
        response = self.client.put(self.contact_detail_url(self.contact.pk), invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_nonexistent_contact(self):
        """
        Test getting a contact that does not exist.
        """
        response = self.client.get(self.contact_detail_url(999), format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_nonexistent_contact(self):
        """
        Test deleting a contact that does not exist.
        """
        response = self.client.delete(self.contact_detail_url(999), format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)