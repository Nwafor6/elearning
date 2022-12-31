# from rest_framework import serializers 
# from accounts.models import CustomUser
# from commonapps.models import Cohort, Track, Course, Module, Answers, LearnerScores, Learner, Announcement


# class UserSerializer(serializers.ModelSerializer):

# 	class Meta:
# 		fields=['email', 'first_name', 'last_name','password', ]
# 		model=CustomUser
# 		extra_kwargs={'password':{'write_only':True}}

# 	def create(self, validate_data):
# 		user=CustomUser(
# 			email=validate_data['email'],
# 			first_name=validate_data['first_name'],
# 			last_name=validate_data['last_name'],
# 			is_admin=True,
# 			is_superuser=True,
# 			is_staff=True
# 			)
# 		user.set_password(validate_data['password'])

# 		user.save()
# 		return user

# class CohortSerializer(serializers.ModelSerializer):

# 	class Meta:
# 		fields='__all__'
# 		model=Cohort

# class TrackSerializer(serializers.ModelSerializer):

# 	class Meta:
# 		fields='__all__'
# 		model=Track

# class CourseSerializer(serializers.ModelSerializer):
	
# 	class Meta:
# 		fields=['track','title','description','course_img','total_point',]
# 		model=Course

# 	def create(self, validate_data):
# 		course=Course.objects.create(
# 			cohort=Cohort.objects.latest('id'),
# 			tutor=self.context['request'].user,
# 			title=validate_data['title'],
# 			description=validate_data['description'],
# 			track=validate_data['track'],
# 			course_img=validate_data['course_img'],
# 			total_point=validate_data['total_point']
# 			)
# 		return course



# class LearnerScoresSerializer(serializers.ModelSerializer):

# 	class Meta:
# 		fields='__all__'
# 		model=LearnerScores

# class LearnerSerializer(serializers.ModelSerializer):

# 	class Meta:
# 		fields='__all__'
# 		model=Learner

# # General announcement posting
# class AnnouncementSerializers(serializers.ModelSerializer):
# 	class Meta:
# 		model=Announcement
# 		fields=['title', ]

# 	def create(self, validate_data):
# 		user=self.context['request'].user
# 		post=Announcement.objects.create(

# 			Poster=user,
# 			title=validate_data['title']
# 			)

# 		return post