from rest_framework import serializers 
from accounts.models import CustomUser
from commonapps.models import Track, Course
from commonapps.serializers import CourseSerializer
from rest_framework.response import Response

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


class TrackSerializer(serializers.ModelSerializer):
	class Meta:
		models=Track
		fields=('title',)


class UserSerializer(serializers.ModelSerializer):
	interest=CourseSerializer(many=True, required=False)
	paid=serializers.BooleanField(required=False)
	phone_numuber=serializers.CharField(max_length=20,required=False)
	gender=serializers.CharField(max_length=20,required=False)
	github_repo=serializers.URLField(required=False)
	linkedln_profile=serializers.URLField(required=False)
	twitter_profile=serializers.URLField(required=False)
	class Meta:
		fields=["id",'email', 'first_name', 'last_name','password', 'paid','phone_numuber','gender','github_repo','linkedln_profile','twitter_profile','interest','slug','started_on','joined',]
		model=CustomUser
		extra_kwargs={'slug':{'read_only':True},'started_on':{'read_only':True},'joined':{'read_only':True},'password':{'write_only':True},}

	def create(self, validated_data):
		_user=self.context['request'].user
		interest=validated_data.pop('interest', None)
		user=CustomUser(
			email=validated_data['email'],
			first_name=validated_data['first_name'],
			last_name=validated_data['last_name'],
			is_learner=True,
			is_active=False

			)
		user.set_password(validated_data['password'])
		# DEACTIVATE USER TO ACTIVATE VIA EMAIL 
		to_email=validated_data['email']
		subject="Account Activation "
		user.save()
		# current_site=self.context['request'].domain
		uid=urlsafe_base64_encode(force_bytes(user.pk))
		token=account_activation_token.make_token(user)

		# Message to be send to the user 
		message=f'''
			This is for testing mode. Copy the uid which is an harshed id of the user and  
			also, copy the token. send the  token and uid to the activate account route to activate the user's account 
			udi:{uid}, token:{token}
		
		'''
		msg= EmailMultiAlternatives(subject, message,'info@scholarsjoint.com.ng',[to_email])
		msg.send()
		# End mail sending

		user.save()
		if interest:
			for single_intrest in interest:
				user.interest.add(single_intrest.id)
				course=Course.objects.get(id=single_intrest.id)
				course.enrolled_users.add(_user.id)
				course.save()
		user.save()


		return user
class UpdateUserSerializer(serializers.ModelSerializer):
	interest=CourseSerializer(many=True, required=False)
	paid=serializers.BooleanField(required=False)
	phone_numuber=serializers.CharField(max_length=20,required=False)
	gender=serializers.CharField(max_length=20,required=False)
	github_repo=serializers.URLField(required=False)
	linkedln_profile=serializers.URLField(required=False)
	twitter_profile=serializers.URLField(required=False)
	class Meta:
		fields=["id",'email', 'first_name', 'last_name','password', 'paid','phone_numuber','gender','github_repo','linkedln_profile','twitter_profile','interest','slug','started_on','joined',]
		model=CustomUser
		extra_kwargs={'slug':{'read_only':True},'started_on':{'read_only':True},'joined':{'read_only':True}}

	# def update(self, instance, validated_data):#instance here is the single user being queried
	# 	_user=self.context['request'].user
	# 	instance.first_name = validated_data.get('first_name', instance.first_name)
	# 	instance.last_name = validated_data.get('last_name', instance.last_name)
	# 	interest=instance.interest.all()#get all the previous courses user has taken registered
	# 	_interest=validated_data.get('interest')

	# 	user=CustomUser(
	# 		# email=validated_data['email'],
	# 		first_name=validated_data['first_name'],
	# 		last_name=validated_data['last_name'],
	# 		paid=validated_data['paid'],
	# 		phone_numuber=validated_data['phone_numuber'],
	# 		gender=validated_data['gender'],
	# 		github_repo=validated_data['github_repo'],
	# 		linkedln_profile=validated_data['linkedln_profile'],
	# 		twitter_profile=validated_data['twitter_profile'],
	# 		# is_learner=True,
	# 		# is_active=False

	# 		)

	# 	if interest:

	# 		for course in interest:#loop and remove the initial courses so as to remove the course the user has unclicked
	# 			instance.interest.remove(course.id)
	# 			course=Course.objects.get(id=course.id)#get the id of each courses and add the user to the enrolled_users
	# 			course.enrolled_users.remove(_user.id)

	# 		for _course in _interest:#loop through the new picked interested courses and add it to the intrested field
	# 			instance.interest.add(_course.id)
	# 			course=Course.objects.get(id=_course.id)#get the id of each courses and add the user to the enrolled_users
	# 			course.enrolled_users.add(_user.id)
	# 			course.save()
	# 	user.save()
	# 	return instance #return the user instance



class StaffsignupSerializer(serializers.ModelSerializer):
	interest=CourseSerializer(many=True, required=False)
	class Meta:
		fields=['email', 'first_name', 'last_name',"password",'slug','is_instructor', 'interest','joined','is_instructor']
		model=CustomUser
		extra_kwargs={'is_instructor':{'read_only':True},'joined':{'read_only':True},'slug':{'read_only':True}}

	def create(self, validated_data):
		interest=validated_data.pop('interest', None)
		user=CustomUser(
			email=validated_data['email'],
			first_name=validated_data['first_name'],
			last_name=validated_data['last_name'],
			is_instructor=True,
			is_active=False

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

		user.save()
		if interest:
			for single_intrest in interest:
				user.interest.add(single_intrest.id)
		user.save()
		return user


class UpdateStaffsignupSerializer(serializers.ModelSerializer):
	interest=CourseSerializer(many=True, required=False)
	class Meta:
		fields=['email', 'first_name', 'last_name','slug','is_instructor', 'interest','joined']
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


