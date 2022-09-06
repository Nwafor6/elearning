from django.urls import path
from rest_framework.routers import SimpleRouter
from .views import TrackViewSet
from .import views


router=SimpleRouter()
router.register('track/', TrackViewSet, basename='track')





urlpatterns=[
	path('users', views.UserApiListView.as_view(), name='users' ),
	path('user/<str:pk>/', views.UserDetail.as_view(), name='user'),
	path('cohorts', views.CohortCreateListView.as_view(), name='cohort'),
	path('create-course', views.CreateCourse.as_view(), name='create-course'),
	path('create-post', views.CreateAnnouncement.as_view(), name="create-post")

]+router.urls