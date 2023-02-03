from django.urls import path
from .import views

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="LMS dOC",
      default_version='v1',
      terms_of_service="https://www.scholarsjoint.com.ng",
      contact=openapi.Contact(email="nwaforglory6@gmailcom"),
      license=openapi.License(name="BSD License"),
      description=
      '''<h1>Welcome to Scholarsjoint LMS endpoint Doc:</h1>
      <h1>Quick Description</h1>

      1: To login a user, send a post request to the 'authentication endpoint' with  the following data "email","password"
      2: To logout a user, send a get request to the 'authentication endpoint as well'. No data is required to logout a user.    
      3: When you register a user, a token and uidb64 value is ent to the users email. The uid is the an harshed value of the "users id". 
      The route "activate/uid/token" endpoint takes in these two values and activate the users account. 
      4: To update a users profile, make a request to the "profile/update" endpoint. This end point supports "put, patch, delete" methods
      5:To change users password, send a request with the users email to the "requesttoken/" endpoint, the if the user's
      account is activated and the user exist, a token with th users id harsed as a uuid is sent to the user. With this token,
      This token and Uid has to be sent to the "changepassword/<uidb64>/<token>/" endpoint along side the users new passoword.With  this all set, the users previous
      password will over written. 
      '''
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
# path('', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

path('make_annocement/',views.MakeAnnouncement.as_view()),
path('make_annocement/<str:pk>/', views.RetriveUpdateAnnouncement.as_view()),
path('make_annocement/<str:pk>/delete/', views.DestoryAnnouncement.as_view()),
path("List-all-tracks/", views.ListTrack.as_view()),
path('add-new-track/', views.CreateTrack.as_view()),
path('update-track/<str:pk>/', views.RetriveUpdateTrack.as_view()),
path('create-course/', views.CreateCourse.as_view()),
# allow user featch single course
path("course_detail/<str:pk>/", views.CourseDetailView.as_view()),
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