from django.shortcuts import render
from rest_framework import generics,viewsets
from rest_framework.decorators import api_view
from .serializers import UserSerializer, StaffsignupSerializer , UpdateUserSerializer ,UpdateStaffsignupSerializer ,LoginSerializer
from commonapps.views import MultipleFieldLookupMixin
from .models import CustomUser
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db.models import Q

# User login authentication
from django.contrib.auth import authenticate, login, logout
from django.contrib.messages import get_messages
# 
# IMPORT EXTRA IMPORT TO SEND USERS MAIL TO ACTIVATE THEIR ACCOUNTS
from django.contrib.sites.shortcuts import get_current_site  
from django.utils.encoding import force_bytes, force_text  
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.template.loader import render_to_string  
from .tokens import account_activation_token 
from django.core.mail import EmailMessage 
from django.core.mail import send_mail, BadHeaderError
from django.core.mail import EmailMultiAlternatives
# end
# Create your views here.

class Registraion(generics.ListCreateAPIView):
	queryset=CustomUser.objects.all()
	serializer_class=UserSerializer
	permission_classes=[AllowAny]


class UpdateRegistraion(viewsets.ModelViewSet):
	queryset=CustomUser.objects.all()
	serializer_class=UpdateUserSerializer
	lookup_field = 'slug'
	permission_classes=[IsAuthenticated]

	def get(self, request, *args, **kwargs):
		user=CustomUser.objects.get(slug=self.kwargs['slug'])
		serializer=self.serializer_class(user, many=False)
		# self.queryset=user

		return Response(serializer.data)

	
# staff registration
class StaffRegistraion(generics.ListCreateAPIView):
	queryset=CustomUser.objects.all()
	serializer_class=StaffsignupSerializer
	permission_classes=[AllowAny]

	def get (self, request, *args, **kwargs):
		users=CustomUser.objects.filter(Q(is_staff=True) | Q(is_instructor=True))
		serializer=self.serializer_class(users, many=True)
		return Response(serializer.data)

# staff registration
class UpdateStaffRegistraion(viewsets.ModelViewSet):
	queryset=CustomUser.objects.all()
	lookup_field = 'slug'
	serializer_class=UpdateStaffsignupSerializer
	permission_classes=[AllowAny]


# class AcivateAccountView(generics.UpdateAPIView):
	# serializer_class=ActivateAccountSerializer
@api_view(['GET'])
def AcivateAccountView(request, uidb64, token):
	try:
		uid=force_text(urlsafe_base64_decode(uidb64))
		user=CustomUser.objects.get(pk=uid)
	except(TypeError, ValueError, OverflowError):
		user=None
		# return Response("Activation link not valid or has expired !!") 
	if user is not None and account_activation_token.check_token(user, token):  
		user.is_active = True  
		user.save()
		return Response("Account Activated !!!") 
	return Response("Activation link not valid or has expired !!")


# Login and logout authentications
class LoginLogoutView(generics.CreateAPIView):
	serializer_class=LoginSerializer

	def get(self, request, *args, **kwargs):
		logout(request)
		return Response("Logout successful !")

	def post(self, request, *args, **kwargs):
		email=request.POST["email"]
		password=request.POST["password"]

		try: 
			user=CustomUser.objects.get(email=email)
		except:
			return Response("User does not exist")
		user= authenticate(request, email=email, password=password)
		if user is not None:
			login(request, user)
			return Response("Login Successful")
		else:
			return Response("User does not exits or invalid credentials")




