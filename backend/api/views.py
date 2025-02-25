from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import FormSerializer
from . import models
from rest_framework.authtoken.models import Token  # our CustomTokenAuthentication works with this model

# Create your views here.

class SignupView(APIView):
    def post(self, request, format=None):
        email = request.data.get("email")
        password = request.data.get("password")
        if not email or not password:
            return Response({"error": "email and password required"}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(username=email).exists():
            return Response({"error": "User with this email already exists"}, status=status.HTTP_400_BAD_REQUEST)
        # Use email as the username.
        user = User.objects.create_user(username=email, email=email, password=password)
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key}, status=status.HTTP_201_CREATED)

class LoginView(APIView):
    def post(self, request, format=None):
        # Expecting the email to be provided in the "username" field as it's used as username.
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            return Response({"error": "username and password required"}, status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(username=username, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_200_OK)
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

class FormView(APIView):
    def get(self, request, pk=None):
        if pk:
            try:
                form = models.Form.objects.get(pk=pk)
            except models.Form.DoesNotExist:
                return Response({"error": "Form not found"}, status=status.HTTP_404_NOT_FOUND)
            serializer = FormSerializer(form)
            return Response(serializer.data)
        forms = models.Form.objects.all()
        serializer = FormSerializer(forms, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = FormSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            form = models.Form.objects.get(pk=pk)
        except models.Form.DoesNotExist:
            return Response({"error": "Form not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = FormSerializer(form, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)