from rest_framework import serializers 
from .models import Announcement, Track, Course, Content, Module,Answers, LearnerScores
from accounts.models import CustomUser 
from api.serializers import ModifiedUserSerializer,ModifiedStaffsignupSerializer
# from accounts import serializers 

class AnnouncementSerializer(serializers.ModelSerializer):
	class Meta:
		model=Announcement
		fields=['title','body']

class TrackSerializers(serializers.ModelSerializer):
	class Meta:
		model=Track
		fields=['title','id']


class CourseSerializer(serializers.ModelSerializer):
	track=TrackSerializers(many=False,)
	tutor=ModifiedStaffsignupSerializer(many=False, required=False)
	enrolled_users=ModifiedUserSerializer(many=True, required=False)
	class Meta:
		model=Course
		fields=['id','tutor','track','title','description','duration','level','course_img','total_point','slug','enrolled_users']
		extra_kwargs={'id':{'read_only':True},'slug':{'read_only':True},'created':{'read_only':True}}


class ModuleSerializer(serializers.ModelSerializer):
	# course=CourseSerializer(many=False)
	class Meta:
		model=Module
		fields=['id','course','title','body','point','slug','posted']
		extra_kwargs={'id':{'read_only':True},'slug':{'read_only':True},'posted':{'read_only':True}}

class ContentSerializer(serializers.ModelSerializer):

	class Meta:
		model=Content
		fields=['module','text','image','video','id']
		extra_kwargs={'id':{'read_only':True},}

class AnswerSerializer(serializers.ModelSerializer):

	class Meta:
		model=Answers
		fields=['content','url','id']
		extra_kwargs={'id':{'read_only':True},}

class GradeLearnerSerializer(serializers.ModelSerializer):

	class Meta:
		model=LearnerScores
		fields=['learner','answers','score','graded_on','id']
		extra_kwargs={'id':{'read_only':True},'graded_on':{'read_only':True},'learner':{'read_only':True},}



