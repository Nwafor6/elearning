from django.contrib import admin
from .models import Track, Course, Module,Content, Answers, LearnerScores,  Announcement

admin.site.register(Track)
admin.site.register(Course)
admin.site.register(Module)
admin.site.register(Answers)
admin.site.register(LearnerScores)
admin.site.register(Announcement)
admin.site.register(Content)