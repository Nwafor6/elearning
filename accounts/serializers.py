from rest_framework import serializers 
from accounts.models import CustomUser
from commonapps.models import Track, Course
from commonapps.serializers import CourseSerializer
from rest_framework.response import Response
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

# # import for jwt customisation
# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
# from rest_framework_simplejwt.views import TokenObtainPairView


class TrackSerializer(serializers.ModelSerializer):
	class Meta:
		model=Track
		fields=('title',)


class UserSerializer(serializers.ModelSerializer):
	interest=CourseSerializer(many=True, required=False)
	# track=TrackSerializer(many=False, required=False)
	paid=serializers.BooleanField(required=False)
	phone_numuber=serializers.CharField(max_length=20,required=False)
	gender=serializers.CharField(max_length=20,required=False)
	github_repo=serializers.URLField(required=False)
	linkedln_profile=serializers.URLField(required=False)
	twitter_profile=serializers.URLField(required=False)
	class Meta:
		fields=["id",'email', 'first_name', 'last_name','password','track','paid','phone_numuber','gender','github_repo','linkedln_profile','twitter_profile','interest','slug','started_on','joined',]
		model=CustomUser
		extra_kwargs={'interest':{'read_only':True},'slug':{'read_only':True},'started_on':{'read_only':True},'joined':{'read_only':True},'password':{'write_only':True},}

	def create(self, validated_data):
		_user=self.context['request'].user
		interest=validated_data.pop('interest', None)
		user=CustomUser(
			email=validated_data['email'],
			first_name=validated_data['first_name'],
			last_name=validated_data['last_name'],
			track=validated_data['track'],
			is_learner=True,
			is_active=False

			)
		user.set_password(validated_data['password'])
		# DEACTIVATE USER TO ACTIVATE VIA EMAIL 
		to_email=validated_data['email']
		# subject="Account Activation "
		subject="Scholarsjoint Skill Aquisition 1.0"
		user.save()
		# current_site=self.context['request'].domain
		uid=urlsafe_base64_encode(force_bytes(user.pk))
		token=account_activation_token.make_token(user)

		# # Message to be send to the user 
		# message=f'''
		# 	This is for testing mode. Copy the uid which is an harshed id of the user and  
		# 	also, copy the token. send the  token and uid to the activate account route to activate the user's account 
		# 	udi:{uid}, token:{token}
		
		# '''
		message=f'''Dear {user.first_name} {user.last_name} \n Thank you for your interest, we have recorded your response and we will get back to you in 24hrs.
		
		'''
		msg= EmailMultiAlternatives(subject, message,'info@scholarsjoint.com.ng',[to_email])
		msg.send()

		# # End mail sending

		user.save()
		users_track=validated_data['track']
		# if interest:
		# 	for single_intrest in interest:
		# 		user.interest.add(single_intrest.id)
		# 		course=Course.objects.get(id=single_intrest.id)
		# 		course.enrolled_users.add(_user.id)
		# 		course.save()
		# user.save()
		if users_track:
			try:
				track=Track.objects.get(title=users_track)
				
			except:
				return Response({"error":"No such track"},status=status.HTTP_400_BAD_REQUEST)
			course=track.course_set.all()
			for single_intrest in course:
				user.interest.add(single_intrest.id)
				course=Course.objects.get(id=single_intrest.id)
				course.enrolled_users.add(user.id)
				course.save()
		user.save()
		return user

class UpdateUserSerializer(serializers.ModelSerializer):
	# Track=TrackSerializer(many=False, required=False)
	# paid=serializers.BooleanField(required=False)
	phone_numuber=serializers.CharField(max_length=20,required=False)
	# gender=serializers.CharField(max_length=20,required=False)
	github_repo=serializers.URLField(required=False)
	linkedln_profile=serializers.URLField(required=False)
	# twitter_profile=serializers.URLField(required=False)
	class Meta:
		fields=["id",'first_name', 'last_name','phone_numuber','github_repo','linkedln_profile','slug','started_on','joined',]
		model=CustomUser
		extra_kwargs={'slug':{'read_only':True},'started_on':{'read_only':True},'joined':{'read_only':True}}


class StaffsignupSerializer(serializers.ModelSerializer):
	interest=CourseSerializer(many=True, required=False)
	# track=TrackSerializer(many=False, required=False)
	class Meta:
		fields=['email', 'first_name', 'last_name',"password",'slug','is_instructor','track', 'interest','joined','is_instructor']
		model=CustomUser
		extra_kwargs={'interest':{'read_only':True},'is_instructor':{'read_only':True},'joined':{'read_only':True},'slug':{'read_only':True}}

	def create(self, validated_data):
		interest=validated_data.pop('interest', None)
		print(validated_data)
		user=CustomUser(
			email=validated_data['email'],
			first_name=validated_data['first_name'],
			last_name=validated_data['last_name'],
			is_instructor=True,
			is_active=False,
			track=validated_data['track'],

			)
		user.set_password(validated_data['password'])
		user.save()

		# DEACTIVATE USER TO ACTIVATE VIA EMAIL 
		to_email=validated_data['email']
		subject="Account Activation "
		# current_site=self.context['request'].domain
		uid=urlsafe_base64_encode(force_bytes(user.pk))
		token=account_activation_token.make_token(user)
		# message to be sent to the user
		message=f'''
			This is for testing mode. Copy the uid which is an harshed id of the user and  
			also, copy the token. send the  token and uid to the activate account route to activate the user's account 
			udi:{uid}, token:{token}
		
		'''
		msg= EmailMultiAlternatives(subject, message,'info@scholarsjoint.com.ng',[to_email])
		msg.send()
		# End mail sending

		# user.save()
		# if interest:
		# 	for single_intrest in interest:
		# 		user.interest.add(single_intrest.id)
		# user.save()
		# return user
		user.save()
		users_track=validated_data['track']
		if users_track:
			try:
				track=Track.objects.get(title=users_track)
				
			except:
				return Response({"error":"No such track"},status=status.HTTP_400_BAD_REQUEST)
			course=track.course_set.all()
			for single_intrest in course:
				user.interest.add(single_intrest.id)
				course=Course.objects.get(id=single_intrest.id)
				course.enrolled_users.add(user.id)
				course.save()
		user.save()
		return user



class UpdateStaffsignupSerializer(serializers.ModelSerializer):
	class Meta:
		fields=['first_name', 'last_name','slug','is_instructor','joined']
		model=CustomUser
		extra_kwargs={'is_instructor':{'read_only':True},'joined':{'read_only':True},'slug':{'read_only':True}}


class LoginSerializer(serializers.Serializer):
	email=serializers.EmailField(required=False)
	password=serializers.CharField(max_length=100, required=False)

class RequestPasswordTokenSerializer(serializers.Serializer):
	email=serializers.EmailField()

class NewPasswordSerializer(serializers.Serializer):
	new_password=serializers.CharField(max_length=100)


class ContactTeamSerializer(serializers.Serializer):
	name=serializers.CharField(max_length=100, required=True)
	# track=serializers.CharField(max_length=100,required=False)
	email=serializers.EmailField(required=True)
	subject=serializers.CharField(max_length=100, required=True)
	message=serializers.CharField(max_length=500, required=True)

class UpdateStduentPaidStatusSerializer(serializers.ModelSerializer):
	class Meta:
		model=CustomUser
		fields=['paid',]
		


	

