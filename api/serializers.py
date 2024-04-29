from django.contrib.auth.models import User 
from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import Task, Contact, Subtask


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'last_name', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
    
class EmailAuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        # Versuche, den Benutzer anhand der E-Mail-Adresse zu finden
        user = authenticate(username=User.objects.get(email=data['email']).username, password=data['password'])
        if not user:
            raise serializers.ValidationError("Unable to log in with provided credentials.")
        return {'user': user}
    
class TaskItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        
    def create(self, validated_data):
        taskslist = Task.objects.create(
            priority=validated_data['priority'],
            title=validated_data['title'],
            description=validated_data['description'],
            due_date=validated_data['due_date'],
            created_at=validated_data['created_at'],
            status=validated_data['status'],
            user=self.context['request'].user  
        )
        return taskslist
    
class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'
        
    def create(self, validated_data):
        contact = Contact.objects.create(
            name=validated_data['name'],
            surname=validated_data['surname'],
            email=validated_data['email'],
            number=validated_data['number']
        )
        return contact
    
    
class SubtaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        
    def create(self, validated_data):
        subtask = Subtask.objects.create(
            title=validated_data['title']
        )
        return subtask 