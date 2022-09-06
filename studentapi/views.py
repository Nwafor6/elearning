from django.shortcuts import render
from accounts.models import CustomUser
from rest_framework import generics
from rest_framework.decorators import api_view
from .serializers import *
from commonapps.models import Track, Course, Learner
from django.shortcuts import get_object_or_404


# Create your views here.

class StudentSignUpView(generics.CreateAPIView):

	serializer_class=StudentUserSerializer

# @api_view(['POST'])
# def LearnerCouseRegSerializerView(request):
# 	serializer=LearnerCouseRegSerializer(data=request.data)
# 	print(serializer)

class LearnerCouseRegSerializerView(generics.CreateAPIView):

	serializer_class=LearnerCouseRegSerializer

class LearnerCouseeditSerializerView(generics.UpdateAPIView):
	queryset=Learner.objects.all()
	serializer_class=LearnerCouseRegSerializer

# submit answer to a module
class ModuleAnswerView(generics.CreateAPIView):

	serializer_class=ModuleAnswer

