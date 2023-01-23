from django.urls import path
from .import views
from rest_framework.routers import SimpleRouter

router=SimpleRouter()
router.register('myprofile/update', views.UpdateRegistraion),
router.register('tutor/profile/update', views.UpdateStaffRegistraion)


urlpatterns=[

	path('registration/', views.Registraion.as_view(), name="registration"),
	path("update-student-paid-status/<slug>/", views.UpdateStudentPaidStatus.as_view()),
	path('registration/staff/', views.StaffRegistraion.as_view()),
	path("activate/<uidb64>/<token>/", views.AcivateAccountView),
	path("login-logout/", views.LoginLogoutView.as_view()),
	path("request-password-reset/", views.SendUserPasswordToken.as_view()),
	path("changepassword/<uidb64>/<token>/", views.ChangeUserPassword.as_view()),
	path("contactteam/", views.ContactTeamView.as_view())
]+router.urls

