from django.db import models
from django.contrib.auth.models import AbstractUser
from django.template.defaultfilters import slugify
from django.conf import settings
from .managers import CustomUserManager
from commonapps.models import Cohort, Course
from . import utils

# Create your models here.





class CustomUser(AbstractUser):
	username=None
	email=models.EmailField(unique=True)
	is_learner=models.BooleanField(default=False)
	is_instructor=models.BooleanField(default=False)
	is_admin = models.BooleanField(default=False)
	slug=models.SlugField(blank=True, unique=True)
	cohort=models.ForeignKey(Cohort, on_delete=models.SET_NULL, blank=True, null=True)
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





