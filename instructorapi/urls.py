from django.urls import path
from .import views







urlpatterns=[
	path('instrcutorsignup/', views.InstrcutorSignUpView.as_view(), name='instrcutorsignup'),
	path('ireg-course/', views.InstrcutorCourse.as_view(), name='ireg-course'),
	path('create-module/', views.ICourseModuleView.as_view(), name='create-module'),
	path('edit-module/<str:pk>/', views.ICourseModuleeditView.as_view(), name='edit-module'),
	path('delete-module/<str:pk>/', views.ICourseModuledeleteView.as_view(), name='delete-module'),
	path('grade-student/', views.IGradingView.as_view(), name='grade-student'),
	path('edit-grade/<str:pk>/', views.IEditGradingView.as_view(), name='edit-grade'),
	path('delete-grade/<str:pk>/', views.IDeleteGradingView.as_view(), name='delete-grade'),

]