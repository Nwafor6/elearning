from django.shortcuts import render
from rest_framework import generics
from commonapps.models import Module
from .serializers import *

# Create your views here.

class InstrcutorSignUpView(generics.CreateAPIView):

	serializer_class=InstructorSerializer

class InstrcutorCourse(generics.CreateAPIView):

	serializer_class=InstructorIntrest

class ICourseModuleView(generics.ListCreateAPIView):
	queryset=Module.objects.all()
	serializer_class=ICourseModule

class ICourseModuleeditView(generics.RetrieveUpdateAPIView):
	queryset=Module.objects.all()
	serializer_class=ICourseModule	

class ICourseModuledeleteView(generics.RetrieveDestroyAPIView):
	queryset=Module.objects.all()
	serializer_class=ICourseModule	