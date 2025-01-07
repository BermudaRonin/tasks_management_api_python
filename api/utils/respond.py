from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND

# Successful responses

def created_data(data = {}):
    return Response(data, status=HTTP_201_CREATED)

def retreived_data(data = {}):
    return Response(data, status=HTTP_200_OK)

def updated_data():
    return Response(status=HTTP_204_NO_CONTENT)

def deleted_data():
    return Response(HTTP_204_NO_CONTENT)

# Error responses

def bad_request(error = "Bad request"):
    return Response({"error": error}, status=HTTP_400_BAD_REQUEST)

def validation_error(error = "Invalid data"):
    return Response({"error": error}, status=HTTP_400_BAD_REQUEST)

def not_found(error = "Not found"):
    return Response({"error": error}, status=HTTP_404_NOT_FOUND)