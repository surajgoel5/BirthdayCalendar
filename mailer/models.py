from django.db import models
from model_utils import Choices
from django.utils import timezone
# Create your models here.
class MailedList(models.Model):
   MAIL_TYPE = Choices(
        (1, 'gen_reminder', 'GEN_REMINDER'), #general reminder
        (2, 'lm_reminder', 'LM_REMINDER'),  # Last minuite reminder
        (3, 'wishday', 'WISHDAY'),  #the day you wish
    )
   type = models.IntegerField(default=MAIL_TYPE.gen_reminder, choices=MAIL_TYPE)
   date= models.DateTimeField(default=timezone.localtime)
   def __str__(self):
       return str(self.type)+"_"+str(self.date.date())

class Logs(models.Model):
    date = models.DateTimeField(default=timezone.localtime)
    log=models.CharField(max_length=500)

    def __str__(self):
        return '['+str(self.date.date())+'] '+self.log

class Lock(models.Model):
    LOCK_STATE= Choices(
        (1, 'aquired', 'AQUIRED'),
        (0, 'released', 'RELEASED')
    )
    lock = models.IntegerField(default=LOCK_STATE.aquired, choices=LOCK_STATE)

    def __str__(self):
        return "LOCK:"+str(self.lock)