from rest_framework import serializers 
from accounts.models import CustomUser
from commonapps.models import Cohort, Track, Course, Module,Answers, LearnerScores, Learner
from api.serializers import TrackSerializer, CourseSerializer


	

class CourseSerializer(serializers.ModelSerializer):

	class Meta:
		fields='__all__'
		model=Course


class TrackSerializer(serializers.ModelSerializer):
	course=CourseSerializer(many=True)
	class Meta:
		fields='__all__'
		model=Track


class StudentUserSerializer(serializers.ModelSerializer):
	class Meta:
		model=CustomUser
		fields=['email', 'first_name', 'last_name','password' ]
		extra_kwargs={'password':{'write_only':True}}

	def create(self, validate_data):
		cohort=Cohort.objects.latest('id')
		user=CustomUser(
			email=validate_data['email'],
			first_name=validate_data['first_name'],
			last_name=validate_data['last_name'],
			is_learner=True,
			cohort=cohort,
			)
		user.set_password(validate_data['password'])

		user.save()
		return user

class LearnerCouseRegSerializer(serializers.ModelSerializer):
	# course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all(), write_only=True,many=True)
	class Meta:
		fields=['course']
		model=Learner

	def create(self, validate_data):
		user=self.context['request'].user
		learner=Learner.objects.create(
			learner=user,
			course=validate_data['course']
			)
		learner.save()
		return learner

# Allow them post anser to module assignments

class ModuleAnswer(serializers.ModelSerializer):
	class Meta:
		model=Answers
		fields=['module','url',]
	def create(self, validate_data):
		answer=Answers.objects.create(
			learner=self.context['request'].user,
			module=validate_data['module'],
			url=validate_data['url']
			)
		return answer
	



