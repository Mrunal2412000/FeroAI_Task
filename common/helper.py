from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from django.utils import translation
import threading
from django.conf import settings
    
def send_response(request, message, data):
    response = JsonResponse(data={"message": message,"data":data})
    response.status_code = 200
    return response

def send_response_validation(request, message):

    response = JsonResponse(data={"message": message})
    response.status_code = 200
    return response

def error_404(request, code, message):

    response = JsonResponse(data={'responseCode': code, 'responseMessage': message})
    response.status_code = 404
    return response

def error_400(request, message):

    response = JsonResponse(data={'message': message})
    response.status_code = 400
    return response

def correct_200(request, message):

    response = JsonResponse(data={'message': message})
    response.status_code = 200
    return response

def error_401(request, message):

    response = JsonResponse(data={'message': message})
    response.status_code = 401
    return response
