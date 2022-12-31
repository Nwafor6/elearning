from rest_framework import serializers 
from .models import Announcement, Track, Course, Content, Module,Answers, LearnerScores


class AnnouncementSerializer(serializers.ModelSerializer):
	class Meta:
		model=Announcement
		fields=['title','body']

class TrackSerializers(serializers.ModelSerializer):
	class Meta:
		model=Track
		fields=['title','id']


class CourseSerializer(serializers.ModelSerializer):

	class Meta:
		model=Course
		fields=['id','tutor','track','title','description','course_img','total_point','slug','enrolled_users']
		extra_kwargs={'id':{'read_only':True},'slug':{'read_only':True},'created':{'read_only':True}}
# class CourseSerializer(serializers.ModelSerializer):

# 	class Meta:
# 		model=Course
# 		fields=['course','title','body','point','slug']

class ModuleSerializer(serializers.ModelSerializer):

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

