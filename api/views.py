from django.shortcuts import render
from rest_framework import generics
from .permissions import IsAuthorOrReadOnly 

from accounts.models import CustomUser
from commonapps.models import Cohort, Track, Course, Module,Answers, LearnerScores, Learner
from .serializers import *
from rest_framework import viewsets
# from .permissions import IsAuthorOrReadOnly
# Create your views here.


class UserApiListView(generics.ListCreateAPIView):
	queryset=CustomUser.objects.all()
	serializer_class=UserSerializer

class UserDelete(generics.RetrieveDestroyAPIView):
	queryset=CustomUser.objects.all()
	serializer_class=UserSerializer


# class UserDetail(generics.RetrieveUpdateDestroyAPIView):
# 	permission_classes = (IsAuthorOrReadOnly,)
# 	queryset=CustomUser.objects.all()
# 	serializer_class=UserSerializer

class CohortCreateListView(generics.ListCreateAPIView):
	queryset=Cohort.objects.all()
	serializer_class=CohortSerializer

class TrackViewSet(viewsets.ModelViewSet):

	queryset=Track.objects.all()
	serializer_class=TrackSerializer

class CreateCourse(generics.ListCreateAPIView):
	queryset=Course.objects.all()
	serializer_class=CourseSerializer

class CreateAnnouncement(generics.ListCreateAPIView):
	queryset=Announcement.objects.all()
	model=Announcement
	serializer_class=AnnouncementSerializers

class EditAnnouncement(generics.RetrieveUpdateAPIView):
	queryset=Announcement.objects.all()
	serializer_class=AnnouncementSerializers

class DeleteAnnouncement(generics.RetrieveDestroyAPIView):
	queryset=Announcement.objects.all()
	serializer_class=AnnouncementSerializers


