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
   date= models.DateTimeField(default=timezone.now)
   def __str__(self):
       return str(self.type)+"_"+str(self.date.date())