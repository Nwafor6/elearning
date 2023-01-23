from django.shortcuts import render
from rest_framework import generics,viewsets
from rest_framework.decorators import api_view
from .serializers import UserSerializer,ContactTeamSerializer, UpdateStduentPaidStatusSerializer,StaffsignupSerializer , RequestPasswordTokenSerializer,NewPasswordSerializer,UpdateUserSerializer ,UpdateStaffsignupSerializer ,LoginSerializer
from commonapps.views import MultipleFieldLookupMixin
from .models import CustomUser
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db.models import Q

# User login authentication
from django.contrib.auth import authenticate, login, logout
from django.contrib.messages import get_messages

# #custom simplejet 
# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
# from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status

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
# Import my custom permissions
from .permissions import IsStaffOnly

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
		return Response({"success":"Account Activated !!!"}) 
	return Response({"error":"Activation link not valid or has expired !!"},status=status.HTTP_400_BAD_REQUEST)


# Login and logout authentications
class LoginLogoutView(generics.CreateAPIView):
	serializer_class=LoginSerializer

	def get(self, request, *args, **kwargs):
		logout(request)
		return Response({"response":"Logout successful !"})

	def post(self, request, *args, **kwargs):
		email=request.data["email"]
		password=request.data["password"]

		try: 
			user=CustomUser.objects.get(email=email)
			serializer=UserSerializer(user, many=False)
			token=RefreshToken.for_user(user)
		except:
			return Response({"error":"User does not exist"}, status=status.HTTP_404_NOT_FOUND)
		user= authenticate(request, email=email, password=password)
		if user is not None:
			login(request, user)
			return Response({"user_data":serializer.data, "access_token":str(token.access_token),}, status=status.HTTP_200_OK)
		else:
			return Response({"error":"invalid credentials"},status=status.HTTP_403_FORBIDDEN)

class SendUserPasswordToken(generics.CreateAPIView):
	serializer_class=RequestPasswordTokenSerializer

	def post(self, request, *args, **kwargs):
		email=request.data['email']
		try:

			user=CustomUser.objects.get(email=email)
		except:
			return Response({"error":"User with this email does not exist !"},status=status.HTTP_404_NOT_FOUND)
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
			return Response({"success":"Reset link sent check your mail"})
			
		else:
			return Response({"error":"Your account is not activated yet so you cannot change your poassword"},status=status.HTTP_403_FORBIDDEN)

class ChangeUserPassword(generics.CreateAPIView):
	serializer_class=NewPasswordSerializer

	def post(self,request, *args, **kwargs):
		uidb64=self.kwargs["uidb64"]
		token=self.kwargs["token"]
		new_password= request.data["new_password"]

		try:
			uid=force_text(urlsafe_base64_decode(uidb64))
			user=CustomUser.objects.get(pk=uid)
		except(TypeError, ValueError, OverflowError):
			user=None
		if user is not None and account_activation_token.check_token(user, token):
			user.set_password(new_password)
			user.save()
			return Response({"success":"Passowrd change successfully"})
		return Response({"error":"Unable to chnage password due to incorrect token"},status=status.HTTP_403_FORBIDDEN)	


class ContactTeamView(generics.CreateAPIView):
	serializer_class=ContactTeamSerializer

	def post(self, request, *args, **kwargs):
		serializer= self.serializer_class(data=request.data)
		if serializer.is_valid():
			name=serializer.data["name"]
			email=serializer.data["email"]
			# track=serializer.data["track"]
			subject=serializer.data["subject"]
			message=serializer.data["message"]
			msg= EmailMultiAlternatives(subject, message,'info@scholarsjoint.com.ng',[email])
			msg.send()
			return Response({"success":"Message sent !!"})
		return Response({"error":"Error ! Make sure your email is valid."},status=status.HTTP_400_BAD_REQUEST)

class UpdateStudentPaidStatus(generics.RetrieveUpdateAPIView):
	queryset=CustomUser.objects.all()
	serializer_class=UpdateStduentPaidStatusSerializer
	permission_classes=[IsStaffOnly, IsAuthenticated]
	lookup_field = 'slug'

	def patch(self, request, *args, **kwargs):
		user=CustomUser.objects.get(slug=self.kwargs["slug"])
		status=request.data["paid"]
		user.paid=status
		user.save()
		serializer=self.serializer_class(user, many=False)
		return Response({"detail":"paid status updated successfully", "user":serializer.data})

# mytoken=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjc0NDUyMTI5LCJpYXQiOjE2NzQ0NDg1MjksImp0aSI6IjBlMTE3MGNiZTlhYjQ5Y2M5ZmJhZjMzMjNiNGYzYjM2IiwidXNlcl9pZCI6MX0.v1R4B5IPrAqbV0UMpeUTjY4Jz5r5655gJG-M1Uan6jk

