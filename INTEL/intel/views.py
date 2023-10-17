from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import (CustomTokenObtainPairSerializer, UserSignupSerializer,
                          ContactUsSerializer, HelpandSupportSerializer, RequestDemoSerializer, UserProfileSerializer)
from .models import CustomUser, Contact, HelpandSupport, RequestDemo, UserProfile
from .utils import (send_verification_email_request_demo, send_verification_email_contact,
                    send_verification_email_help_and_support)
from rest_framework import viewsets, serializers, viewsets, status, permissions, generics



class UserSignupViewSet(APIView):
    """
    User Signup
    """
    serializer_class = UserSignupSerializer
    queryset = CustomUser.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            # Valid data, create a new user
            user = serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Extends the default TokenObtainPairView to add the user's details to the response,
    saving an additional request after login.
    """

    serializer_class = CustomTokenObtainPairSerializer

class LogoutView(APIView):
    permission_classes = [permissions.AllowAny]

    def custom_logout(self, request):
        logout(request)
        return JsonResponse({'message': 'Logout successful'})


class RequestDemoViewSet(viewsets.ModelViewSet):
    queryset = RequestDemo.objects.all()
    serializer_class = RequestDemoSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        send_verification_email_request_demo(instance)

class ContactUsViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactUsSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        send_verification_email_contact(instance)


class HelpandSupportViewSet(viewsets.ModelViewSet):
    queryset = HelpandSupport.objects.all()
    serializer_class = HelpandSupportSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        send_verification_email_help_and_support(instance)


class UserProfileList(generics.ListCreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

class UserProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer