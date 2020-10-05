from django.urls import path,include
from . import views


urlpatterns = [
path('start/', views.start)
]


from mailer.tasks import *
import datetime
from background_task.models import *
from django.conf import settings

Task.objects.all().delete()
CompletedTask.objects.all().delete()

mailerFunc(schedule=1,repeat=60*20, repeat_until=None)