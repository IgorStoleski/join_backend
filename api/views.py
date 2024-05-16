from django.shortcuts import render
from django.contrib.auth.models import User 
from rest_framework import generics
from .serializers import UserSerializer
from rest_framework.authtoken.views import ObtainAuthToken, APIView, Token, Response
from rest_framework import status
from django.contrib.auth import logout
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Task, Contact, Subtask
from .serializers import TaskItemSerializer, ContactSerializer, SubtaskSerializer, EmailAuthTokenSerializer
from rest_framework.exceptions import NotFound


class UserView(APIView):
    """
    View for creating and retrieving User instances.

    Provides two HTTP methods:
    - POST: To create a new user instance.
    - GET: To retrieve one or all user instances.
    """
    def post(self, request):
        """
        Creates a new user instance.
        Args:
            request (HttpRequest): The request object containing the user data.

        Returns:
            Response: A Django Rest Framework response object with the created user data and HTTP 201 Created status on success.
            If the data is invalid, returns a response with error details and HTTP 400 Bad Request status.
        """
        """ serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) """
        print("Incoming request data:", request.data)  # Debug-Log
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print("Serializer errors:", serializer.errors)  # Debug-Log
        return Response({'success': False, 'message': 'Validation errors', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, pk=None, format=None):
        """
        Retrieves user instance(s).
        Args:
            request (HttpRequest): The request object.
            pk (int, optional): The primary key of the user to retrieve. Defaults to None.
            format (str, optional): The format of the response (e.g., 'json'). Defaults to None.

        Returns:
            Response: A Django Rest Framework response object containing the user data.
            If a specific user is requested and not found, raises NotFound with a 404 status.
        """
        if pk:
            try:
                user = User.objects.get(pk=pk)
                serializer = UserSerializer(user)
            except User.DoesNotExist:
                raise NotFound(detail="User not found", code=404)
        else:
            users = User.objects.all()
            serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    
class TasksItemView(APIView):
    """
    View to interact with Task instances.
    * Requires token authentication.
    * Only authenticated users are able to access this view.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None, format=None):
        """
        Retrieve a single Task by its id or all Tasks if no id is provided.

        Args:
            request: The HTTP request object.
            pk: The primary key of the Task instance to retrieve.
            format: The format of the response (defaults to JSON if None).

        Returns:
            Response object containing serialized Task data.
        """
        if pk:
            try:
                todo = Task.objects.get(pk=pk)  # Einzelnen Task abrufen
                serializer = TaskItemSerializer(todo)
            except Task.DoesNotExist:
                raise NotFound(detail="Task not found", code=404)
        else:
            todos = Task.objects.all()  # Alle Tasks abrufen
            serializer = TaskItemSerializer(todos, many=True)
        return Response(serializer.data)
    
    
    def post(self, request, format=None):
        """
        Create a new Task instance from provided data.
        Args:
            request: The HTTP request object.
            format: The format of the response (defaults to JSON if None).

        Returns:
            Response object with created Task data and HTTP 201 status on success,
            or error details with HTTP 400 status on failure.
        """
        serializer = TaskItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
         
    def put(self, request, pk=None, format=None):
        """
        Update an existing Task specified by its id with provided data.

        Args:
            request: The HTTP request object.
            pk: The primary key of the Task to update.
            format: The format of the response (defaults to JSON if None).

        Returns:
            Response object with updated Task data, or error details with HTTP 400 status on failure.
        """
        if pk:
            try:
                todo = Task.objects.get(pk=pk)
                serializer = TaskItemSerializer(todo, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Task.DoesNotExist:
                raise NotFound(detail="Task not found", code=404)
        else:
            return Response({"message": "Missing task ID"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        """
        Delete a Task instance specified by its id.

        Args:
            request: The HTTP request object.
            pk: The primary key of the Task to delete.
            format: The format of the response (defaults to JSON if None).

        Returns:
            Empty Response object with HTTP 204 status on successful deletion.
        """
        todo = Task.objects.get(pk=pk, author=request.user)
        todo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
   
    
class LoginView(ObtainAuthToken):
    """
    View for handling user authentication requests by verifying email and password,
    and returning an authentication token.
    
    Attributes:
        serializer_class (serializer instance): Specifies the serializer used for
        validating and deserializing input data. It handles email-based authentication.
    """
    serializer_class = EmailAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests to authenticate a user.        
        Processes the incoming data through the defined serializer to validate user credentials.
        If credentials are valid, an authentication token is either retrieved or created for
        the user, and the token along with user details are returned.
        Args:
            request (HttpRequest): The request object containing all the data sent with the POST request.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        Returns:
            Response: A response object containing the authentication token, user's ID, and email address
            if the authentication is successful. If credentials are invalid, raises an exception with
            appropriate error messages.        
        Raises:
            ValidationError: An error indicating what went wrong during user validation.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })
        

class LogoutView(APIView):
    """
    A view that handles log out operations for authenticated users.
    This view handles POST requests to log out a user by clearing their session and
    returning an HTTP 204 No Content status, indicating that the server successfully
    processed the request, but is not returning any content.
    Methods:
        post(request): Handles the POST request to log out a user.
    """
    def post(self, request):
        """
        Handle the POST request to log out a user.
        This method logs out the user by calling the `logout` function, which clears
        the user's session. After the user is logged out, the method returns an empty
        response with a 204 No Content status.
        Parameters:
            request (HttpRequest): The request object containing all the details of the request.
        Returns:
            Response: An HTTP Response object with status 204 No Content.
        """
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class ContactView(APIView):
    """
    A view class to handle CRUD operations for contacts.
    Attributes:
        authentication_classes (list): List of authentication classes for this view.
        permission_classes (list): List of permission classes for this view.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        """
        Handle POST requests to create a new contact.
        Args:
            request (HttpRequest): The HTTP request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        Returns:
            Response: HTTP response containing serialized data of the created contact.
        Raises:
            Response(status=status.HTTP_400_BAD_REQUEST): If the provided data is invalid.
        """
        serializer = ContactSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, pk=None, format=None):
        """
        Handle GET requests to retrieve contacts.
        Args:
            request (HttpRequest): The HTTP request object.
            pk (int, optional): The primary key of the contact to retrieve.
            format (str, optional): The format of the response.
        Returns:
            Response: HTTP response containing serialized data of the requested contact(s).
        Raises:
            NotFound: If the requested contact does not exist.
        """
        if pk:
            try:
                user = Contact.objects.get(pk=pk)
                serializer = ContactSerializer(user)
            except Contact.DoesNotExist:
                raise NotFound(detail="User not found", code=404)
        else:
            users = Contact.objects.all()
            serializer = ContactSerializer(users, many=True)  
        return Response(serializer.data)
    
    def put(self, request, pk=None, *args, **kwargs):
        """
        Handle PUT requests to update an existing contact.
        Args:
            request (HttpRequest): The HTTP request object.
            pk (int, optional): The primary key of the contact to update.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        Returns:
            Response: HTTP response containing serialized data of the updated contact.
        Raises:
            NotFound: If the contact to be updated does not exist.
            Response(status=status.HTTP_400_BAD_REQUEST): If the provided data is invalid.
        """
        if pk:
            try:
                contact = Contact.objects.get(pk=pk)
                serializer = ContactSerializer(contact, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Contact.DoesNotExist:
                raise NotFound(detail="Contact not found", code=404)
        else:
            return Response({"message": "Missing contact ID"}, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk=None, *args, **kwargs):
        """
        Handle DELETE requests to delete an existing contact.
        Args:
            request (HttpRequest): The HTTP request object.
            pk (int, optional): The primary key of the contact to delete.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        Returns:
            Response: HTTP response indicating the success of the deletion.
        Raises:
            NotFound: If the contact to be deleted does not exist.
        """
        if pk:
            try:
                contact = Contact.objects.get(pk=pk)
                contact.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            except Contact.DoesNotExist:
                raise NotFound(detail="Contact not found", code=404)
        else:
            return Response({"message": "Missing contact ID"}, status=status.HTTP_400_BAD_REQUEST)
    
    
class SubtaskItemView(APIView):
    """
    A view to handle CRUD operations for individual subtasks.    
    Methods:
    - get(self, request, pk=None, format=None): Retrieve a single subtask or a list of all subtasks.
    - post(self, request, format=None): Create a new subtask.
    - put(self, request, pk, format=None): Update an existing subtask.
    - delete(self, request, pk, format=None): Delete an existing subtask.
    """
    def get(self, request, pk=None, format=None):
        """
        Retrieve a single subtask or a list of all subtasks.
        Args:
            request: The request object.
            pk (int, optional): The primary key of the subtask to retrieve. Defaults to None.
            format (str, optional): The format of the response. Defaults to None.
        Returns:
            Response: A JSON response containing the serialized subtask(s).
        """
        if pk:
            try:
                subtask = Subtask.objects.get(pk=pk)
                serializer = SubtaskSerializer(subtask)
            except Subtask.DoesNotExist:
                raise NotFound(detail="Subtask not found", code=404)
        else:
            subtasks = Subtask.objects.all()
            serializer = SubtaskSerializer(subtasks, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        """
        Create a new subtask.
        Args:
            request: The request object.
            format (str, optional): The format of the response. Defaults to None.
        Returns:
            Response: A JSON response containing the created subtask data.
        """
        serializer = SubtaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk, format=None):
        """
        Update an existing subtask.
        Args:
            request: The request object.
            pk (int): The primary key of the subtask to update.
            format (str, optional): The format of the response. Defaults to None.
        Returns:
            Response: A JSON response containing the updated subtask data.
        """
        subtask = Subtask.objects.get(pk=pk)
        serializer = SubtaskSerializer(subtask, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        """
        Delete an existing subtask.
        Args:
            request: The request object.
            pk (int): The primary key of the subtask to delete.
            format (str, optional): The format of the response. Defaults to None.
        Returns:
            Response: An empty response indicating successful deletion.
        """
        subtask = Subtask.objects.get(pk=pk)
        subtask.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)