from django.urls import path,include
from . import views


urlpatterns = [
path('start/', views.start)
]


from mailer.tasks import *
test() 
#mailerFunc()