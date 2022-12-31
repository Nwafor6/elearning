from django.shortcuts import render
from rest_framework import generics
from commonapps.models import Module


#list all the contents in the instructors's registered course modules
# @api_view(['GET'])
# def I_courseModulesContents(request, slug):
# 	my_modules=Module.objects.get(slug=slug)
# 	if request.user in my_modules.course.enrolled_users.all()
# 		content=my_modules.content_set.all()
# 		serializer=ContentSerializer(content, many=True)
# 		return Response(serializer.data)
# 	return Response('error !! you did not register for this course')

