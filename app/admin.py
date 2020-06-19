from django.contrib import admin
from .models import Question, myUser, Answer, Tag, Like, Dislike

admin.site.register(Question)
admin.site.register(myUser)
admin.site.register(Answer)
admin.site.register(Tag)
admin.site.register(Like)
admin.site.register(Dislike)