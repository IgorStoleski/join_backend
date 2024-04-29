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
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, pk=None, format=None):
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
    """ authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated] """

    def get(self, request, pk=None, format=None):
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
        serializer = TaskItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
         
    def put(self, request, pk, format=None):
        todo = Task.objects.get(pk=pk, author=request.user)
        serializer = TaskItemSerializer(todo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        todo = Task.objects.get(pk=pk, author=request.user)
        todo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
   
    
class LoginView(ObtainAuthToken):
    serializer_class = EmailAuthTokenSerializer

    def post(self, request, *args, **kwargs):
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
    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class ContactView(APIView):
    """ authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated] """
    
    def post(self, request, *args, **kwargs):
        serializer = ContactSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, pk=None, format=None):
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
    def get(self, request, pk=None, format=None):
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
        serializer = SubtaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk, format=None):
        subtask = Subtask.objects.get(pk=pk)
        serializer = SubtaskSerializer(subtask, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        subtask = Subtask.objects.get(pk=pk)
        subtask.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)