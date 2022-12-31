# from django.shortcuts import render
# from accounts.models import CustomUser
# from rest_framework import generics
# from rest_framework.decorators import api_view
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response
# from .serializers import *
# from commonapps.models import Track, Course, Learner
# from django.shortcuts import get_object_or_404
# from api.permissions import IsAuthorOrReadOnly


# # Create your views here.

# class StudentSignUpView(generics.CreateAPIView):

# 	serializer_class=StudentUserSerializer



# # Allow only authenticated learners to register for a course
# class LearnerCouseRegSerializerView(generics.CreateAPIView):
# 	serializer_class=LearnerCouseRegSerializer
# 	# prevent only uthenticated users to register for a course
# 	permission_class=[IsAuthenticated]

# 	def get(self, request, format=None):
		
# 		content = {
# 			'status': 'request was permitted'
# 		}
# 		return Response(content)


# # Resrict learners to only change the course they registered for only
# class LearnerCouseeditSerializerView(generics.RetrieveUpdateAPIView):
# 	queryset=Learner.objects.all()
# 	serializer_class=LearnerCouseRegSerializer

# 	# permission_class=[IsAuthorOrReadOnly]

# 	# def get(self, request, format=None):
		
# 	# 	content = {
# 	# 		'status': 'request was permitted'
# 	# 	}
# 	# 	return Response(content)
# 	def get_queryset(self):
# 		user=self.request.user
# 		return Learner.objects.filter(learner=user)

# # submit answer to a module
# # restrict learners to only courses the egistered for
# class ModuleAnswerView(generics.CreateAPIView):

# 	serializer_class=ModuleAnswer

# 	permission_class=[IsAuthenticated]

# 	def get(self, request, format=None):
		
# 		content = {
# 			'status': 'request was permitted'
# 		}
# 		return Response(content)

	


