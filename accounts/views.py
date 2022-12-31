from django.shortcuts import render
from rest_framework import generics
from .serializers import UserSerializer, StaffsignupSerializer
from commonapps.views import MultipleFieldLookupMixin
from .models import CustomUser
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db.models import Q
# Create your views here.

class Registraion(generics.ListCreateAPIView):
	queryset=CustomUser.objects.all()
	serializer_class=UserSerializer
	permission_classes=[AllowAny]

class UpdateRegistraion(MultipleFieldLookupMixin,generics.RetrieveUpdateAPIView):
	queryset=CustomUser.objects.all()
	serializer_class=UserSerializer
	lookup_fields = ['slug']
	permission_classes=[IsAuthenticated]

	def get(self, request, *args, **kwargs):
		user=CustomUser.objects.get(slug=self.kwargs['slug'])
		serializer=self.serializer_class(user, many=False)
		# self.queryset=user

		return Response(serializer.data)

	
# staff registration
class StaffRegistraion(generics.ListCreateAPIView):
	queryset=CustomUser.objects.all()
	serializer_class=StaffsignupSerializer
	permission_classes=[AllowAny]

	def get (self, request, *args, **kwargs):
		users=CustomUser.objects.filter(Q(is_staff=True) | Q(is_instructor=True))
		serializer=self.serializer_class(users, many=True)
		return Response(serializer.data)


