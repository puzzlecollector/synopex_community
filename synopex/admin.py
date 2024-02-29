from django.contrib import admin
from .models import Question, Board
# Register your models here.

class QuestionAdmin(admin.ModelAdmin):
    search_fields = ['subject']


admin.site.register(Board)
admin.site.register(Question, QuestionAdmin)