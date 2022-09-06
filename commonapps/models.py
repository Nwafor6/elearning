from django.db import models
from django.conf import settings
from django.template.defaultfilters import slugify

# Create your models here.



class Announcement(models.Model):
	Poster=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True,blank=True)
	title=models.CharField(max_length=50, unique=True)
	# body=models.TextField()
	posted=models.DateTimeField(auto_now_add=True, blank=True, null=True)

	def __str__(self):
		return self.title

class Cohort(models.Model):
	title=models.CharField(max_length=50, unique=True)


	def __str__(self):
		return self.title

class Track(models.Model):
	title=models.CharField(max_length=50, unique=True)
	



	def __str__(self):
		return self.title



class Course(models.Model):
	tutor=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True,blank=True)
	cohort=models.ForeignKey(Cohort, on_delete=models.CASCADE)
	track=models.ForeignKey(Track, on_delete=models.CASCADE)
	title=models.CharField(max_length=200)
	description=models.TextField()
	course_img=models.ImageField(blank=True, null=True)
	total_point=models.PositiveIntegerField(default=100)
	slug=models.SlugField(max_length=200, unique=True)
	created =models.DateTimeField(auto_now_add=True)



	class Meta:        
		ordering = ['title']

	def __str__(self):        
		return self.title


	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug=slugify(self.title)
		super(Course, self).save(*args,**kwargs)


class Module(models.Model):    
	course = models.ForeignKey(Course,on_delete=models.CASCADE)
	title = models.CharField(max_length=200)
	body= models.TextField(blank=True, null=True)
	point=models.PositiveIntegerField(default=10)
	posted=models.DateTimeField(auto_now_add=True, blank=True, null=True)
	closing_date=models.DateTimeField(blank=True, null=True,)


	def __str__(self):        
		return self.title

class Answers(models.Model):
	learner=models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	module = models.ForeignKey(Module,on_delete=models.CASCADE,  blank=True,null=True)
	url=models.CharField(max_length=200)


	def __str__(self):
		return f"{self.learner} | {self.url}"


class LearnerScores(models.Model):
	learner=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
	answers = models.ForeignKey(Answers,on_delete=models.CASCADE, null=True, blank=True)
	score=models.PositiveIntegerField(default=0)
	graded_on=models.DateTimeField(auto_now_add=True,blank=True, null=True)

	def __str__(self):
		return f"{self.learner} | {self.score}"	

class Learner(models.Model):
	learner=models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	course = models.OneToOneField(Course,on_delete=models.SET_NULL, blank=True, null=True)
	total_scores=models.PositiveIntegerField(default=0)


	def __str__(self):
		return f"{self.learner} | {self.course}"	

class Instructor(models.Model):
    instructor =models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ManyToManyField(Course,)


    def __str__(self):
    	return f"{self.instructor} | {self.course}"	



	

