from rest_framework import serializers 
from accounts.models import CustomUser
from commonapps.models import Cohort, Track, Course, Module,Answers, LearnerScores, Learner, Instructor


class InstructorSerializer(serializers.ModelSerializer):

	class Meta:
		fields=['email', 'first_name', 'last_name','password', ]
		model=CustomUser
		extra_kwargs={'password':{'write_only':True}}

	def create(self, validate_data):
		user=CustomUser(
			email=validate_data['email'],
			first_name=validate_data['first_name'],
			last_name=validate_data['last_name'],
			is_instructor=True
			)
		user.set_password(validate_data['password'])

		user.save()
		return user


class InstructorIntrest(serializers.ModelSerializer):
	
	class Meta:
		model=Instructor
		fields=['course']


	def create(self, validate_data):
		user=self.context['request'].user
		course=validate_data['course']
		instructor=Instructor.objects.create(
			instructor=user,
			)
		instructor.course.set(course)
		return instructor

# Instructor able to create module for course

class ICourseModule(serializers.ModelSerializer):

	class Meta:
		model=Module
		fields=['course','title','body','point', 'closing_date']
