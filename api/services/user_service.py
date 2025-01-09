from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from api.serializers import UserSerializer
from api.utils import respond, validate

# User Management Service Layer

def create_user(user_data):
    """
    Create a new user.
    
    Args:
        user_data (dict): Data for creating the user.
        
    Returns:
        Response: Created user data or validation error.
    """
    serializer = UserSerializer(data=user_data)
    if serializer.is_valid():
        serializer.save()
        return respond.created_data(serializer.data)
    return respond.validation_error(serializer.errors)

def get_user(user):
    """
    Retrieve user details.
    
    Args:
        user (User): User instance to retrieve.
        
    Returns:
        Response: Retrieved user data.
    """
    serializer = UserSerializer(user)
    return respond.retreived_data(serializer.data)

def update_user(user, user_data):
    """
    Update user information.
    
    Args:
        user (User): User instance to update.
        user_data (dict): Data to update.
        
    Returns:
        Response: Updated user response or validation error.
    """
    serializer = UserSerializer(user, data=user_data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return respond.updated_data()
    return respond.validation_error(serializer.errors)

def delete_user(user):
    """
    Delete a user.
    
    Args:
        user (User): User instance to delete.
        
    Returns:
        Response: Confirmation of deletion.
    """
    user.delete()
    return respond.deleted_data()

def authenticate_user(user_credentials):
    """
    Authenticate user and generate an auth token.
    
    Args:
        user_credentials (dict): User credentials (username and password).
        
    Returns:
        Response: Authentication token and user data or error response.
    """
    # Validate user credentials
    is_valid, validation_error = validate.user_credentials(user_credentials)
    if not is_valid:
        return respond.validation_error(validation_error)
    
    # Authenticate user
    user = authenticate(username=user_credentials['username'], password=user_credentials['password'])
    if not user:
        return respond.not_found("Incorrect credentials")

    # Generate or retrieve existing token
    token, _ = Token.objects.get_or_create(user=user)
    
    serializer = UserSerializer(user)
    return respond.retreived_data({"token": token.key, "user": serializer.data})
