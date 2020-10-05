from django.urls import path,include
from . import views


urlpatterns = [
path('start/', views.start)
]


from mailer.tasks import *
import datetime
from background_task.models import Task

mailerFunc(schedule=1,repeat=60*1, repeat_until=None)