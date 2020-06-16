from django.contrib import admin
from .models import Question, User, Answer, Tag, Like, Dislike

admin.site.register(Question)
admin.site.register(User)
admin.site.register(Answer)
admin.site.register(Tag)
admin.site.register(Like)
admin.site.register(Dislike)