import django


from django.urls import path
from . import views

#
urlpatterns = [
    path('', views.index, name="getTopic"),
    path('topic', views.topic, name='topic'),
    path('questions', views.questions, name='questions'),
]
