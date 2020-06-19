from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from django.contrib import admin

from app import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('ask/', views.ask, name='ask'),
    path('hot/', views.hot, name='hot'),
    path('tag/<str:tag_name>/', views.tag, name='tag'),
    path('question/<int:qid>/', views.question, name='question'),
    path('signup/', views.signup, name='signup'),
    path('settings/', views.settings, name='settings'),
    path('admin/', admin.site.urls),
    path('f/', views.fake), # Faker data
]
