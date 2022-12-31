from .serializers import AnnouncementSerializer, TrackSerializers, CourseSerializer ,ModuleSerializer, ContentSerializer,AnswerSerializer,GradeLearnerSerializer
from .models import Announcement, Track , Course, Content, Module, Answers, LearnerScores
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import generics
from django.shortcuts import get_object_or_404
from accounts.models import CustomUser

# @api_view(['POST'])
# def make_addnocement(request):
# 	if request.method == "POST":
# 		print(request.data['title'])
# 	return Response('Hello')

class MultipleFieldLookupMixin:
    """
    Apply this mixin to any view or viewset to get multiple field filtering
    based on a `lookup_fields` attribute, instead of the default single field filtering.
    """
    def get_object(self):
        queryset = self.get_queryset()             # Get the base queryset
        queryset = self.filter_queryset(queryset)  # Apply any filter backends
        filter = {}
        for field in self.lookup_fields:
            if self.kwargs[field]: # Ignore empty fields.
                filter[field] = self.kwargs[field]
        obj = get_object_or_404(queryset, **filter)  # Lookup the object
        self.check_object_permissions(self.request, obj)
        return obj



class MakeAnnouncement(generics.ListCreateAPIView):
	queryset=Announcement.objects.all()
	serializer_class=AnnouncementSerializer
	permission_classes=[IsAuthenticated]


	def get(self, request, *args, **kwargs):
		serializer=self.serializer_class(Announcement.objects.filter(Poster=request.
			user) ,many=True)
		return Response(serializer.data)

	def post(self, request, *args, **kwags):
		announcement=Announcement.objects.create(title=request.data['title'], body=request.data['body'], Poster=request.user)
		serializer=self.serializer_class(announcement)
		return Response(serializer.data)


class RetriveUpdateAnnouncement(generics.RetrieveUpdateAPIView):
	queryset=Announcement.objects.all()
	serializer_class=AnnouncementSerializer
	permission_classes=[IsAuthenticated]


class DestoryAnnouncement(generics.DestroyAPIView):
	queryset=Announcement.objects.all()
	serializer_class=AnnouncementSerializer

	def delete(self, request, *args, **kwargs):
		self.object = self.get_object()
		self.object.delete()
		return Response('success')

class CreateListTrack(generics.ListCreateAPIView):
	queryset=Track.objects.all()
	serializer_class=TrackSerializers
	permission_classes=[IsAuthenticated]

class RetriveUpdateTrack(generics.RetrieveUpdateAPIView):
	queryset=Track.objects.all()
	serializer_class=TrackSerializers
	permission_classes=[IsAuthenticated]

# list and create courses by tutors only
# add tutor permission classs to this view
class CreateCourse(generics.ListCreateAPIView):
	queryset=Course.objects.all()
	serializer_class=CourseSerializer
	permission_classes=[IsAuthenticated]



	# if request.user.is_learner:
	def get(self, request, *args, **kwargs):
		serializer=self.serializer_class(Course.objects.all(),many=True)
		return Response(serializer.data)


# list all courses only without creating both for learners and tutors
class AllCoursesView(generics.ListAPIView):
	queryset=Course.objects.all()
	serializer_class=CourseSerializer
	permission_classes=[IsAuthenticated]

# list courses based on the requesting tutor
class MyCourses(generics.ListAPIView):
	queryset=Course.objects.all()
	serializer_class=CourseSerializer
	permission_classes=[IsAuthenticated]



	# if request.user.is_learner:
	def get(self, request, *args, **kwargs):
		serializer=self.serializer_class(Course.objects.filter(tutor=request.user),many=True)
		return Response(serializer.data)


# list courses based on the requesting student
class MyRegisteredCourses(generics.ListAPIView):
	queryset=Course.objects.all()
	serializer_class=CourseSerializer
	permission_classes=[IsAuthenticated]

	# if request.user.is_learner:
	def get(self, request, *args, **kwargs):
		all_courses=Course.objects.all()
		my_registered_courses=[my_course for my_course in all_courses if request.user in my_course.enrolled_users.all()]
		serializer=self.serializer_class(my_registered_courses,many=True)
		return Response(serializer.data)

#list all the module in the student's registered course
@api_view(['GET'])
def my_courseModules(request, slug):
	my_learning=Course.objects.get(slug=slug)
	if request.user in my_learning.enrolled_users.all():
		modules=my_learning.module_set.all()
		serializer=ModuleSerializer(modules, many=True)
		return Response(serializer.data)
	return Response('error !! you did not register for this course')

#list all the contents in the student's registered course modules
@api_view(['GET'])
def my_courseModulesContents(request, slug):
	my_modules=Module.objects.get(slug=slug)
	if request.user in my_modules.course.enrolled_users.all():
		content=my_modules.content_set.all()
		serializer=ContentSerializer(content, many=True)
		return Response(serializer.data)
	return Response('error !! you did not register for this course')


#Allow user click from a list of course after registration and add it to their course interest.
@api_view(['GET','POST'])
def AddToMyCourses(request):
	user=request.user
	_User=CustomUser.objects.get(email=user)
	if request.method == "POST":
		try:
			slug=request.data['slug']
		except:
			return Response('slug error!. slug must be in json format')
		course=Course.objects.get(slug=slug)
		print(slug)
		if request.user in course.enrolled_users.all():#check if the user has this course and uneroll the person.
			course.enrolled_users.remove(_User)
			_User.interest.remove(course.id)
			return Response("You have already unenrolled for this course")
		# If they dont have this course, add course to interest and addd them to the erolled user of the course
		course.enrolled_users.add(_User)
		_User.interest.add(course.id)
		_User.save()
		return Response("Course added successfully !")
	allcourses=Course.objects.all()
	serializer=CourseSerializer(allcourses, many=True)
	return Response (serializer.data)


class UpdateRegisterCourse(MultipleFieldLookupMixin,generics.RetrieveUpdateAPIView):
	queryset=Course.objects.all()
	serializer_class=CourseSerializer
	lookup_fields = ['slug']
	permission_classes=[IsAuthenticated]

	def get(self, request, *args, **kwargs):
		course=Course.objects.get(slug=self.kwargs['slug'])
		# print(request.user in course.enrolled_users.all())
		# print(course.enrolled_users.all())
		serializer=self.serializer_class(Course.objects.get(slug=self.kwargs['slug']))
		return Response(serializer.data)

class CreateCourseModule(generics.ListCreateAPIView):
	queryset=Module.objects.all()
	serializer_class=ModuleSerializer
	permission_classes=[IsAuthenticated]

	
class UpdateCourseModule(MultipleFieldLookupMixin,generics.RetrieveUpdateAPIView):
	queryset=Module.objects.all()
	serializer_class=ModuleSerializer
	lookup_fields = ['slug']
	permission_classes=[IsAuthenticated]



class DeleteCourseModule(MultipleFieldLookupMixin,generics.DestroyAPIView):
	queryset=Module.objects.all()
	serializer_class=ModuleSerializer
	lookup_fields = ['slug']
	permission_classes=[IsAuthenticated]


	def delete(self, request, *args, **kwargs):
		self.object = self.get_object()
		self.object.delete()
		return Response('Module deleted successfully !')


class CreateModuleContent(generics.ListCreateAPIView):
	queryset=Content.objects.all()
	serializer_class=ContentSerializer
	permission_classes=[IsAuthenticated]

class UpdateModuleContent(MultipleFieldLookupMixin, generics.RetrieveUpdateAPIView):
	queryset=Content.objects.all()
	serializer_class=ContentSerializer
	lookup_fields = ['pk']
	permission_classes=[IsAuthenticated]

class DeleteModuleContent(MultipleFieldLookupMixin,generics.DestroyAPIView):
	queryset=Content.objects.all()
	serializer_class=ModuleSerializer
	lookup_fields = ['pk']
	permission_classes=[IsAuthenticated]


	def delete(self, request, *args, **kwargs):
		self.object = self.get_object()
		self.object.delete()
		return Response("Module's content deleted successfully !")


class PostContentAnswer(generics.ListCreateAPIView):
	queryset=Answers.objects.all()
	serializer_class=AnswerSerializer
	permission_classes=[IsAuthenticated]

	def get(self, request, *args, **kwargs):
		serializer=self.serializer_class(Answers.objects.all(),many=True)
		return Response(serializer.data)

	def post(self, request, *args, **kwags):
		content=Content.objects.get(id=request.data['content']) 
		url=request.data['url']
		learner=CustomUser.objects.get(email=request.user)
		if request.user in content.module.course.enrolled_users.all():
			try:
				my_answer=Answers.objects.create(content=content, url=url, learner=learner)
				LearnerScores.objects.create(answers=my_answer, learner=learner)
			except:
				return Response('Error you cannot submit more than once') 
			serializer=self.serializer_class(my_answer)
			return Response(serializer.data)
		return Response('Error ! You do not have this course as your registered course')


class GradeLearnersViews(MultipleFieldLookupMixin, generics.ListCreateAPIView):
	queryset=LearnerScores.objects.all()
	serializer_class=GradeLearnerSerializer
	permission_classes=[IsAuthenticated]

	def post(self, request, *args, **kwags):
		score=request.data['score']
		answer=Answers.objects.get(id=request.data['answers'])
		learner=CustomUser.objects.get(id=answer.learner.id)
		try:
			grade=LearnerScores.objects.create(answers=answer, learner=learner, score=score)
		except:
			return Response('student cannot be gradded twice ')

		serializer=self.serializer_class(grade, many=True)
		return Response(serializer.data)


# @api_view(['GET'])
# def moduleContents(request, slug):
# 	Course=Course.objects.get(slug=slug, user=request.user)
# 	module=course.module_set.all()


