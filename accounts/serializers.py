from rest_framework import serializers 
from accounts.models import CustomUser
from commonapps.models import Track, Course
from commonapps.serializers import CourseSerializer



class TrackSerializer(serializers.ModelSerializer):
	class Meta:
		models=Track
		fields=('title',)


class UserSerializer(serializers.ModelSerializer):
	interest=CourseSerializer(many=True)
	class Meta:
		fields=['email', 'first_name', 'last_name','password', 'interest','slug','started_on','joined',]
		model=CustomUser
		extra_kwargs={'slug':{'read_only':True},'email':{'read_only':True},'password':{'write_only':True},'started_on':{'read_only':True},'joined':{'read_only':True},}

	def create(self, validated_data):
		_user=self.context['request'].user
		interest=validated_data.pop('interest', None)
		user=CustomUser(
			email=validated_data['email'],
			first_name=validated_data['first_name'],
			last_name=validated_data['last_name'],
			is_learner=True,

			)
		user.set_password(validated_data['password'])

		user.save()
		if interest:
			for single_intrest in interest:
				user.interest.add(single_intrest.id)
				course=Course.objects.get(id=single_intrest.id)
				course.enrolled_users.add(_user.id)
				course.save()
		user.save()

		return user

	def update(self, instance, validated_data):#instance here is the single user being queried
		_user=self.context['request'].user
		instance.first_name = validated_data.get('first_name', instance.first_name)
		instance.last_name = validated_data.get('last_name', instance.last_name)
		interest=instance.interest.all()#get all the previous courses user has taken registered
		_interest=validated_data.get('interest')

		for course in interest:#loop and remove the initial courses so as to remove the course the user has unclicked
			instance.interest.remove(course.id)
			course=Course.objects.get(id=course.id)#get the id of each courses and add the user to the enrolled_users
			course.enrolled_users.remove(_user.id)

		for _course in _interest:#loop through the new picked interested courses and add it to the intrested field
			instance.interest.add(_course.id)
			course=Course.objects.get(id=_course.id)#get the id of each courses and add the user to the enrolled_users
			course.enrolled_users.add(_user.id)
			course.save()
		return instance #return the user instance


class StaffsignupSerializer(serializers.ModelSerializer):
	interest=CourseSerializer(many=True)
	class Meta:
		fields=['email', 'first_name', 'last_name','slug','is_instructor','password', 'interest','joined','is_instructor']
		model=CustomUser
		extra_kwargs={'is_instructor':{'read_only':True},'password':{'write_only':True},'joined':{'read_only':True},'slug':{'read_only':True},'email':{'write_only':True}}

	def create(self, validated_data):
		interest=validated_data.pop('interest', None)
		user=CustomUser(
			email=validated_data['email'],
			first_name=validated_data['first_name'],
			last_name=validated_data['last_name'],
			is_instructor=True,
			# is_staff=True

			)
		user.set_password(validated_data['password'])

		user.save()
		if interest:
			for single_intrest in interest:
				user.interest.add(single_intrest.id)
		user.save()
		return user

