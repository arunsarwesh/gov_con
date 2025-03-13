from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from . import models
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.authtoken.models import Token  # our CustomTokenAuthentication works with this model
import random
import secrets
from django.utils import timezone


class SignupOTPView(APIView):
    def post(self, request, format=None):
        email = request.data.get("email")
        if not email:
            return Response({"error": "Email required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            code = str(random.randint(100000, 999999))
            models.SignupOTP.objects.create(email=email, code=code)

            send_mail(
                'Your Signup OTP',
                f'Your OTP for signup is {code}',
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
            
            return Response({"message": "OTP sent to email."}, status=status.HTTP_200_OK)

        except Exception as e:
            
            return Response({"error": f"Failed to send OTP: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SignupView(APIView):
    def post(self, request, format=None):
        email = request.data.get("email")
        otp = request.data.get("otp")
        if not email or not otp:
            return Response({"error": "Email and OTP required"}, status=status.HTTP_400_BAD_REQUEST)
        otp_entry = models.SignupOTP.objects.filter(email=email, code=otp).order_by('-created_at').first()
        if not otp_entry:
            return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)
        otp_entry.delete()
        # Store pending signup details for admin approval
        pending, created = models.PendingSignup.objects.get_or_create(
            email=email,
            name=request.data.get("name"),
            College_Name=request.data.get("CollegeName"),
            role=request.data.get("role"),
            phone=request.data.get("phone"),
            
        )
        admin_email = 'nithishkumarnk182005@gmail.com'
        send_mail(
            'New Signup Approval Needed',
            f'New signup request details: {request.data}',
            "sarweshwardeivasihamani@gmail.com",
            [admin_email],
            fail_silently=False,
        )
        return Response({"message": "Signup request submitted. Await admin approval."}, status=status.HTTP_200_OK)

class ApproveSignupView(APIView):
    def get(self, request):
        pending = models.PendingSignup.objects.filter(is_approved=False)
        serializer = PendingSignupSerializer(pending, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        email = request.data.get("email")
        if not email:
            return Response({"error": "Email required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            pending = models.PendingSignup.objects.get(email=email, is_approved=False)
        except models.PendingSignup.DoesNotExist:
            return Response({"error": "Pending signup not found"}, status=status.HTTP_404_NOT_FOUND)
        pending.is_approved = True
        pending.approved_at = timezone.now()
        pending.save()
        # Generate a very strong password
        strong_password = secrets.token_urlsafe(16)
        user = User.objects.create_user(username=email, email=email, password=strong_password)
        send_mail(
            'Your Account Has Been Approved',
            f'Your account has been approved.\nUsername: {email}\nPassword: {strong_password}',
            "sarweshwardeivasihamani@gmail.com",
            [email],
            fail_silently=False,
        )
        return Response({"message": "User approved and credentials sent."}, status=status.HTTP_200_OK)

class LoginView(APIView):
    def post(self, request, format=None):
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
    
    def delete(self, request, pk):
        try:
            if pk == '000':
                forms = models.Form.objects.all()
                forms.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            form = models.Form.objects.get(pk=pk)
        except models.Form.DoesNotExist:
            return Response({"error": "Form not found"}, status=status.HTTP_404_NOT_FOUND)
        form.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)