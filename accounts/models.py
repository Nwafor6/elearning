from django.db import models
from django.contrib.auth.models import AbstractUser
from django.template.defaultfilters import slugify
from django.conf import settings
from .managers import CustomUserManager
from commonapps.models import Track, Course
from . import utils

# Create your models here.





class CustomUser(AbstractUser):
	username=None
	email=models.EmailField(unique=True)
	is_learner=models.BooleanField(default=False)
	is_instructor=models.BooleanField(default=False)
	is_admin = models.BooleanField(default=False)
	slug=models.SlugField(blank=True, unique=True, null=True)
	track=models.ForeignKey(Track,on_delete=models.SET_NULL, blank=True,null=True)
	interest=models.ManyToManyField(Course,null=True, blank="True")
	started_on=models.DateTimeField(auto_now_add=False, auto_now=False, null=True, blank=True)
	joined=models.DateTimeField(auto_now_add=True)
	paid=models.BooleanField(default=False, blank="")
	phone_numuber=models.CharField(max_length=20, blank="", null=True)
	gender=models.CharField(max_length=20,  null=True, choices=(("Male","Male"),("Female","Female"),("Others","Others")))
	github_repo=models.URLField(blank="", null=True)
	linkedln_profile=models.URLField(blank="",  null=True)
	twitter_profile=models.URLField(blank="", null=True)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS=['first_name', 'last_name']

	objects=CustomUserManager()
	class Meta:
		ordering=['email']
		verbose_name='User'


	def __str_(self):
		return self.email

	def gen_random_slug(self):
		random_slug = slugify(self.first_name + self.last_name + utils.generate_random_id())
		while CustomUser.objects.filter(slug=random_slug).exists():
			random_slug = slugify(self.first_name + self.last_name + utils.generate_random_id())
		return random_slug
        
	def save(self, *args, **kwargs):
        # Check for a slug        
		if not self.slug:
            # Create default slug
			self.slug = self.gen_random_slug()
        # Finally save.
		super().save(*args, **kwargs)

# class UserToken(models.Model):
# 	token=models.CharField(max_length=100)
# 	user=models.OneToOneField(CustomUser, on_delete=models.CASCADE)
# 	token_used=models.BooleanField(default=False)

# 	def __str__(self):
# 		return f"{self.user}, {self.token}"




