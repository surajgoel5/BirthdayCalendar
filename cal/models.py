from django.db import models
from model_utils import Choices
import datetime
import numpy as np
# Create your models here.
class Birthday(models.Model):

    PRIORITIES = Choices(
            (1, 'fam', 'FAM'),  #month
            (2, 'vvip', 'VVIP'), #week
            (3, 'vip', 'VIP'), #day before
            (4, 'gen', 'GEN'), #same day
        )

    priority = models.IntegerField(default=PRIORITIES.gen, choices=PRIORITIES)
    name = models.CharField(max_length=100)
    bday = models.DateField('birthday')
    fblink=models.CharField(max_length=100)
    bdate=models.DateField('birthdate', blank=True,default=datetime.date(1,1,1))
    
    def save(self, *args, **kwargs):
        self.bdate = datetime.date(datetime.MINYEAR,self.bday.month,self.bday.day)
        super(Birthday, self).save(*args, **kwargs)

    def haveAge(self,curr_date):
        self.age=int(np.rint((curr_date-self.bday).days /365))
    def __str__(self):
        return self.name




    