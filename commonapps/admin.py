from django.contrib import admin
from .models import Track, Course, Module, Answers, LearnerScores, Learner, Instructor, Announcement

admin.site.register(Track)
admin.site.register(Course)
admin.site.register(Module)
admin.site.register(Answers)
admin.site.register(LearnerScores)
admin.site.register(Learner)
admin.site.register(Instructor)
admin.site.register(Announcement)