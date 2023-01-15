from django.urls import path
from .import views

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="LMS dOC",
      default_version='v1',
      description="Endpoints description",
      terms_of_service="https://www.scholarsjoint.com.ng",
      contact=openapi.Contact(email="nwaforglory6@gmailcom"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
path('', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

path('make_annocement/',views.MakeAnnouncement.as_view()),
path('make_annocement/<str:pk>/', views.RetriveUpdateAnnouncement.as_view()),
path('make_annocement/<str:pk>/delete/', views.DestoryAnnouncement.as_view()),
path('add-new-track/', views.CreateListTrack.as_view()),
path('update-track/<str:pk>/', views.RetriveUpdateTrack.as_view()),
path('create-course/', views.CreateCourse.as_view()),
# path('update-course/<slug:slug>/',views.UpdateRegisterCourse.as_view()),
path('create-course-module/', views.CreateCourseModule.as_view()),
path('update-course-module/<slug:slug>/',views.UpdateCourseModule.as_view()),
path('delete-course-module/<slug:slug>/',views.DeleteCourseModule.as_view()), 
path('create-module-content/', views.CreateModuleContent.as_view()), 
path('update-module-content/<str:pk>/',views.UpdateModuleContent.as_view()),
path('delete-module-content/<str:pk>/',views.DeleteModuleContent.as_view()),

# list all courses both by students and tutors
path('all-courses/', views.AllCoursesView.as_view()),
# list all courses by a tutors
path('mycourses/', views.MyCourses.as_view()),
# list all courses registeered by a Student
path('mylearning/', views.MyRegisteredCourses.as_view()),
# list all the modules for my specific course
path('my-courses/<slug:slug>/modules', views.my_courseModules),
# list all the contents for my course's moudles
# path('module/<slug:slug>/contents', views.my_courseModulesContents),
path('module/<slug:slug>/contents/', views.my_courseModulesContents),
# allow user click and addd course to their registered course from the course list view
path('buy-course/', views.AddToMyCourses),

# Students Post answers to contents
path('content/submit/answer/', views.PostContentAnswer.as_view()), 
path('gradestudents/', views.GradeLearnersViews.as_view())
]