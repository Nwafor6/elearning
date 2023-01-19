from django.shortcuts import render
from rest_framework import generics,viewsets
from rest_framework.decorators import api_view
from .serializers import UserSerializer,ContactTeamSerializer, StaffsignupSerializer , RequestPasswordTokenSerializer,NewPasswordSerializer,UpdateUserSerializer ,UpdateStaffsignupSerializer ,LoginSerializer
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

class SendUserPasswordToken(generics.CreateAPIView):
	serializer_class=RequestPasswordTokenSerializer

	def post(self, request, *args, **kwargs):
		email=request.POST['email']
		try:

			user=CustomUser.objects.get(email=email)
		except:
			return Response("User with this email does not exist !")
		if user.is_active:
			uid=urlsafe_base64_encode(force_bytes(user.pk))
			token=account_activation_token.make_token(user)
			subject="Passoword Reset Email"
			message=f'''
			This is for testing mode. Copy the uid which is an harshed id of the user and  
			also, copy the token. send the  token and uid to the activate account route to activate the user's account 
			udi:{uid}, token:{token}
		
			'''
			msg= EmailMultiAlternatives(subject, message,'info@scholarsjoint.com.ng',[email])
			msg.send()
			return Response(("Reset link sent check your mail"))
			
		else:
			return Response("Your account is not activated yet so you cannot change your poassword")

class ChangeUserPassword(generics.CreateAPIView):
	serializer_class=NewPasswordSerializer

	def post(self,request, *args, **kwargs):
		uidb64=self.kwargs["uidb64"]
		token=self.kwargs["token"]
		new_password= request.POST["new_password"]

		try:
			uid=force_text(urlsafe_base64_decode(uidb64))
			user=CustomUser.objects.get(pk=uid)
		except(TypeError, ValueError, OverflowError):
			user=None
		if user is not None and account_activation_token.check_token(user, token):
			user.set_password(new_password)
			user.save()
			return Response("Passowrd change successfully")
		return Response("Unable to chnage password due to incorrect token")	


class ContactTeamView(generics.CreateAPIView):
	serializer_class=ContactTeamSerializer

	def post(self, request, *args, **kwargs):
		serializer= self.serializer_class(data=request.data)
		if serializer.is_valid():
			name=serializer.data["name"]
			email=serializer.data["email"]
			track=serializer.data["track"]
			subject=serializer.data["subject"]
			message=serializer.data["message"]
			if track:
				message=f"""
					Track:{track},
					{message}
				"""
			else:
				message=message
			print(message,"jhggy")
			msg= EmailMultiAlternatives(subject, message,'info@scholarsjoint.com.ng',[email])
			msg.send()
			return Response(serializer.data)
		return Response("Error ! Make sure your email is valid.")