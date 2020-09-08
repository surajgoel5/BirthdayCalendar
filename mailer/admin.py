from django.contrib import admin

from .models import *

admin.site.register(MailedList)
admin.site.register(Logs)
admin.site.register(Lock)

# Register your models here.
