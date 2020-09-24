from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from django.shortcuts import render
import datetime
from .models import Birthday
import numpy as np
# Create your views here.

NO_OF_DAYS=12
UPCOMING_BDAY_DAYS=30


def index(request):
    today = timezone.localtime(timezone.now()).date()
    return flipcal(request, today.year, today.month, today.day)


def date_diff(curr,next):  #only input dates not day
    today=curr
    next_date=next
    if next_date<today:
        next_date = datetime.date(today.year+1,next_date.month,next_date.day)
    return (next_date-today).days

def day_to_date(day):
    return datetime.date(datetime.MINYEAR,day.month,day.day)

def getBirthday(date,today):
    high_priority = False
    try:
        bdays= Birthday.objects.filter(bdate=day_to_date(date))
        fbd=bdays[0]

        bday_class = "low_priority_bday"
        for bd in bdays:
            bd.haveAge(today)
            if bd.priority<3:
                high_priority =True
                bday_class = "high_priority_bday"

    except Exception as e:
       
        bdays = None
        bday_class = None

    return {"bdays":bdays,"class":bday_class,"high_priority":high_priority}



def flipcal(request,yy,mm,dd):
    this=datetime.date(yy,mm,dd)
    today = timezone.localtime(timezone.now()).date()
    #this=today
    context={"year":this.year,"month":this.month,"day":this.day}

    date=this- datetime.timedelta(days=this.day-1)

    prev_date=date - datetime.timedelta(days=1)

    context["prev_date"]={"month":prev_date.strftime("%B"),"year":prev_date.strftime("%Y"),"date":prev_date}
    dates=[]
    while date.month==this.month:
        bday=getBirthday(date,this)
        if date>today:
            tense="ing"
        else:
            tense="ed"

        dates.append({"weekday":date.strftime("%A"),"day":date.strftime("%d"),"month":date.strftime("%B"),"bday":bday,"tense":tense} )
        date=date+datetime.timedelta(days=1)
    context["dates"]=dates

    next_date=date
    context["next_date"]={"month":next_date.strftime("%B"),"year":next_date.strftime("%Y"),"date":next_date}
    context["upcoming_bdays"]=getupcoming()
    return render(request, "index.html", context)




def allbdays(request):
    all_birthdays = Birthday.objects.order_by('bdate')
    fw=["600","500","400","100"]
    for bday in all_birthdays:
        bday.fw=fw[bday.priority-1]
    context={"bdays":all_birthdays}

    return render(request, "allbdays.html", context)

def exportallbdays(request):
    all_birthdays = Birthday.objects.order_by('bdate')
    with open("savedBdays.txt", 'w') as file:
        bdays = []
        for bday in all_birthdays:
            file.write(str(bday.priority)+','+bday.name+','+str(bday.bday)+','+str(bday.bdate)+','+bday.fblink+'\n')
    return(HttpResponse("Saved"))

def importallbdays(request):
    file= open("savedBdays.txt", 'r')
    all_birthdays = Birthday.objects.order_by('bdate')
    for line in file:

        pri,name,bday,bdate,fblink=line.split(",")
        fblink = fblink[:-1]
        d_bday=datetime.datetime.strptime(bday, '%Y-%m-%d').date()
        d_bdate=datetime.datetime.strptime(bdate, '%Y-%m-%d').date()
        newbday=Birthday(priority=int(pri),name=name,bday=d_bday,bdate=d_bdate,fblink=fblink)

        if Birthday.objects.filter(name=name,bday=bday, priority=int(pri),bdate=d_bdate,fblink=fblink):
            print("exists",name)
        else:
            newbday.save()
            print("Saved")


    return(HttpResponse("Updated"))

def getupcoming():

    today = timezone.localtime(timezone.now()).date()
    todate = datetime.date(datetime.MINYEAR, today.month, today.day)
    all_birthdays = Birthday.objects.order_by('bdate')
    mindays=367
    upcoming_bdays=[]
    for bday in all_birthdays:
        datediff=date_diff(todate, bday.bdate)
        if datediff<UPCOMING_BDAY_DAYS and datediff>0:
            upcoming_bdays.append(bday)
    return upcoming_bdays
