from django.contrib import admin
from .models import Category Quiz, Question, Option, Attempt, Answer


admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Option)
admin.site.register(Attempt)
admin.site.register(Answer)