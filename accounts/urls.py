from django.urls import path
from .import views


urlpatterns=[

	path('registration/', views.Registraion.as_view(), name="registration"),
	path('myprofile/update/<slug:slug>/', views.UpdateRegistraion.as_view()),
	path('registration/staff/', views.StaffRegistraion.as_view())

]

