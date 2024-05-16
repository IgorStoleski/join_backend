from datetime import datetime
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import Task, Contact, Subtask


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and updating User instances.
    This serializer is responsible for serializing/deserializing User instances
    for use in Django REST Framework views. It includes fields for 'id', 'username',
    'last_name', 'email', and 'password'.
    Attributes:
        model: The User model class to serialize/deserialize.
        fields: The fields to include in the serialization process.
        extra_kwargs: Extra keyword arguments for customizing field behavior.
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        """
        Create a new User instance.
        Args:
            validated_data: A dictionary containing validated data for creating a User.
        Returns:
            User: The newly created User instance.
        Raises:
            KeyError: If any required field is missing in the validated data.
        """
        user = User.objects.create_user(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
    
class EmailAuthTokenSerializer(serializers.Serializer):
    """
    Serializer for authenticating users via email and password.
    Attributes:
        email (serializers.EmailField): The email address of the user.
        password (serializers.CharField): The password of the user.
    Methods:
        validate(self, data): Validates the provided email and password against the user database.
    """
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        """
        Validates the provided email and password against the user database.
        Args:
            data (dict): A dictionary containing 'email' and 'password' keys.
        Returns:
            dict: A dictionary containing a 'user' key if authentication is successful.
        Raises:
            serializers.ValidationError: If provided credentials are invalid.
        """
        user = User.objects.filter(email=data['email']).first()
        if not user:
            raise serializers.ValidationError({'non_field_errors': ['User does not exist.']})
        
        user = authenticate(username=user.username, password=data['password'])
        if not user:
            raise serializers.ValidationError({'non_field_errors': ['Unable to log in with provided credentials.']})

        return {'user': user}
    
class DateOnlyField(serializers.Field):
    """
    A custom serializer field for handling date-only values.
    This field is intended to be used in Django REST Framework serializers to handle
    date-only values in a specific format.
    Attributes:
        format (str): The format string for date representation, default is '%Y-%m-%d'.
    """
    def to_representation(self, value):
        """
        Convert the internal representation to a primitive data type for serialization.
        Args:
            value: The internal representation of the data.
        Returns:
            str: The string representation of the date.
        """
        return value
    
    def to_internal_value(self, data):
        """
        Convert a primitive data type to the internal representation of the field.
        Args:
            data (str): The primitive data type to be converted to the internal representation.
        Returns:
            datetime.date: The internal representation of the date.
        """
        return datetime.strptime(data, '%Y-%m-%d').date()
    
class TaskItemSerializer(serializers.ModelSerializer):
    """
    Serializer for converting Task model instances to JSON format and vice versa.    
    Attributes:
        due_date (DateOnlyField): Custom field for handling date without time.    
    Meta:
        model (Task): The model class to serialize.
        fields (str): Indicates to serialize all fields of the Task model.
    """
    due_date = DateOnlyField()
    class Meta:
        model = Task
        fields = '__all__'
        
    def create(self, validated_data):
        """
        Creates a new Task instance based on the provided validated data.        
        Args:
            validated_data (dict): The validated data to create a new Task instance.            
        Returns:
            Task: The newly created Task instance.
        """
        taskslist = Task.objects.create(
            priority=validated_data['priority'],
            title=validated_data['title'],
            description=validated_data['description'],
            due_date=validated_data['due_date'],
            status=validated_data['status'],
            category=validated_data['category'],
            assignedTo=validated_data['assignedTo'],
            bgcolor=validated_data['bgcolor'],
            subtasks=validated_data['subtasks']
        )
        return taskslist
    
class ContactSerializer(serializers.ModelSerializer):
    """
    Serializer class for Contact model.
    This serializer is used to serialize/deserialize Contact objects.
    Attributes:
        model (class): The Contact model class to serialize/deserialize.
        fields (str or tuple): Specifies the fields to include in the serialization.
    """
    class Meta:
        model = Contact
        fields = '__all__'
        
    def create(self, validated_data):
        """
        Method to create a new Contact instance.
        Args:
            validated_data (dict): Dictionary containing validated data for Contact creation.
        Returns:
            Contact: Newly created Contact instance.
        Raises:
            KeyError: If any required field is missing in validated_data.
        """
        contact = Contact.objects.create(
            name=validated_data['name'],
            surname=validated_data['surname'],
            email=validated_data['email'],
            telefon=validated_data['telefon'],
            bgcolor=validated_data['bgcolor']
        )
        return contact
    
    
class SubtaskSerializer(serializers.ModelSerializer):
    """
    Serializer for Subtask model.
    This serializer handles the serialization and deserialization of Subtask instances.
    """
    class Meta:
        model = Task
        fields = '__all__'
        
    def create(self, validated_data):
        """
        Create and return a new Subtask instance.
        Args:
            validated_data (dict): The validated data for creating the Subtask.
        Returns:
            Subtask: The created Subtask instance.
        Raises:
            KeyError: If the required data for creating the Subtask is missing.
        """
        subtask = Subtask.objects.create(
            title=validated_data['title']
        )
        return subtask 