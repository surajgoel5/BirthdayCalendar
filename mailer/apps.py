from django.apps import AppConfig
import email.message
import email.utils
import smtplib
import time
from django.utils import timezone
import datetime
from operator import itemgetter
from django.template.loader import get_template
import random

EMAIL_ID=os.environ.get('EMAIL_ID');
EMAIL_PASSWORD=os.environ.get('EMAIL_PASS');
EMAIL_TO=os.environ.get('EMAIL_TO');


#reminder days
P1_DAYS=14 #14
P2_DAYS=7#7
P3_DAYS=1#1

#MAil Times in 24hr hrs
GEN_REM_TIME=12
LM_REM_TIME=23
WISH_TIME=18

COLORS=["#2d55e7","#c24ed1","#32e191","#28c3ff"]
color=""
def mailerFunc():
    from .models import Lock
    lock = Lock.objects.filter(id=1)[0]
    lock.lock=1
    lock.save()


    rndtime=random.random()*30
    makeLog("Sleeping for: "+str(rndtime))
    time.sleep(rndtime)
    lock=Lock.objects.filter(id=1)[0]
    if lock.lock:
        lock.lock =0
        lock.save()
        makeLog("Lock Aquired")
    else:
        makeLog("Lock couldn't be aquired, terminating this thread")
        return 0

    from cal.models import Birthday
    from .models import MailedList
    global color

    makeLog("Mailing Normal")
    while True:

        color = COLORS[len(MailedList.objects.order_by('type')) % 4]

        today=timezone.localtime(timezone.now()).date()
        currentHour = datetime.datetime.now().hour
        if currentHour==GEN_REM_TIME:
            if len(MailedList.objects.filter(type=MailedList.MAIL_TYPE.gen_reminder,date__date=today))!=0:
                makeLog("General Reminder for Today has already been sent")
                time.sleep(300)
            else:
                makeLog("Sending todays's gen reminder")
                sendGenReminder(Birthday)
                MailedList(type=MailedList.MAIL_TYPE.gen_reminder).save()

        elif currentHour==LM_REM_TIME:
            if len(MailedList.objects.filter(type=MailedList.MAIL_TYPE.lm_reminder, date__date=today)) != 0:
                makeLog("LM Reminder for Today has already been sent")
                time.sleep(300)
            else:
                makeLog("Sending todays's LM reminder")
                sendLMReminder(Birthday)
                MailedList(type=MailedList.MAIL_TYPE.lm_reminder).save()

        elif currentHour==WISH_TIME:
            if len(MailedList.objects.filter(type=MailedList.MAIL_TYPE.wishday, date__date=today)) != 0:
                makeLog("Wishes already sent")
                time.sleep(300)
            else:
                makeLog("Sending todays's wishes")
                sendWishes(Birthday)
                MailedList(type=MailedList.MAIL_TYPE.wishday).save()

        time.sleep(10)
def makeLog(text):
    from .models import Logs
    Logs(log=text).save()

def sendGenReminder(Birthday):
    reminders = getBirthdayReminders(Birthday)
    if len(reminders)!=0:
        makeLog("Sending Gen Reminders for:" + str(reminders))
        subject,rendered=prepareReminderEmail(reminders)
        send_email(subject,rendered)

def sendLMReminder(Birthday):
    reminders = getBirthdayReminders(Birthday)
    if len(reminders) != 0:
        rems = []
        for rem in reminders:

            if rem[1]==1:

                rems.append(rem)
        makeLog("Sending LM Reminders for:"+str(rems))
        subject,rendered=prepareReminderEmailLM(rems)
        send_email(subject, rendered)

def sendWishes(Birthday):
    bdays=getTodayBirthdays(Birthday)
    if len(bdays)!=0:

        makeLog("Wish "+str(bdays))
        subject, rendered = prepareWishdayEmail(bdays)
        send_email(subject, rendered)

def getBirthdayReminders(Birthday): #mail to be sent at 12noon #call again nad filter remdays to 1 for last minuite wish

    todate = day_to_date(timezone.localtime(timezone.now()).date())
    all_birthdays = Birthday.objects.order_by('bdate')
    reminders=[]
    for bday in all_birthdays:
        remaining_days=(date_diff(todate,bday.bdate)).days
        ##Reminders
        if remaining_days==P1_DAYS and bday.priority==1:
            reminders.append([bday,remaining_days,bday.priority])
        elif remaining_days==P2_DAYS and bday.priority in [1,2]:
            reminders.append([bday,remaining_days,bday.priority])
        elif remaining_days==P3_DAYS and bday.priority in [1,2,3]:
            reminders.append([bday, remaining_days, bday.priority])
    return reminders

def getTodayBirthdays(Birthday):
    todate = day_to_date(timezone.localtime(timezone.now()).date())
    bdays = Birthday.objects.filter(bdate=todate)
    return bdays



def prepareReminderEmail(reminders):
    from cal.views import getupcoming
    no_of_reminders=len(reminders)
    subject="Birthday Reminder!"
    if no_of_reminders==1:
        bday,rem_days,pri=reminders[0]
        fname=bday.name.split(" ")[0]
        title=fname+"'s Birthday is coming soon!"
        if rem_days==P1_DAYS:
            remtime="in <b>2 weeks</b>"
        elif rem_days==P2_DAYS:
            remtime="in <b>1 week</b>"
        else:
            remtime="<b>tomorrow</b>"
        title = fname + "'s Birthday is "+remtime.replace('<b>','').replace('</b>','')+"!"
        p1text="Hey Suraj! <b>"+bday.name+"'s</b> Birthday is due "+remtime+". Don't forget to wish!"

    else:
        title=""
        p1text="Hey Suraj! <br>"
        fnames = []
        bdays = []
        remtimes = []
        for rem in reminders:
            bday, rem_days, pri = rem
            fname = bday.name.split(" ")[0]
            fnames.append(fname)
            bdays.append(bday)
            if rem_days == P1_DAYS:
                remtime = "in <b>2 weeks</b>"
            elif rem_days == P2_DAYS:
                remtime = "in <b>1 week</b>"
            else:
                remtime = "<b>tomorrow</b>"
            remtimes.append(remtime)
        for i in range(no_of_reminders):
            if i==no_of_reminders-1:
                nex = ""
            elif i==no_of_reminders-2:
                nex = " and "
            elif i<no_of_reminders-2:
                nex = ", "
            p1text += "<br>&nbsp;&nbsp;&nbsp; <b>" + fnames[i] + "'s</b> birthday is due " + remtimes[i] + nex+"."
            title+= fnames[i]+nex
        title+=" have birthdays coming soon!"

        p1text += "<br><br>Don't forget to wish them!"

    global color

    context={ 'title': title,'p1text':p1text,'upcoming_bdays':getupcoming(),'color':color }
    template = get_template('email_reminder.html')
    rendered=template.render(context)

    return subject,rendered

def prepareReminderEmailLM(reminders):
    from cal.views import getupcoming
    no_of_reminders=len(reminders)
    title="Wish them before you sleep!"
    p1text="Hey Suraj! <br>"
    fnames = []
    bdays = []
    remtimes = []
    for rem in reminders:
        bday, rem_days, pri = rem
        fname = bday.name.split(" ")[0]
        fnames.append(fname)
        bdays.append(bday)
    singular=""
    if no_of_reminders-1:
        singular="s"
    for i in range(no_of_reminders):
        if i==no_of_reminders-1:
            nex = " "
        elif i==no_of_reminders-2:
            nex = " and "
        elif i<no_of_reminders-2:
            nex = ", "
        p1text+= "<b>"+fnames[i]+"</b>"+nex

    p1text += "have birthday"+singular+" tonight. <br> Don't forget to wish!"
    subject = "Birthday"+singular+" Tonight!"

    context={ 'title': title,'p1text':p1text,'upcoming_bdays':getupcoming() }
    template = get_template('email_reminder_lm.html')
    rendered=template.render(context)
    #f = open("email_temp_gen_text.htm", "w")
    #f.write(rendered)
    #f.close()
    #send_email(subject, message=rendered)
    return subject,rendered


def prepareWishdayEmail(bdays):
    from cal.views import getupcoming
    no_of_bdays=len(bdays)
    title="Wish them a Happy Birthday!"
    p1text="Hey Suraj! <br>"
    fnames = []
    for bday in bdays:
        fname = bday.name.split(" ")[0]
        fnames.append(fname)

    singular=""
    if no_of_bdays-1:
        singular="s"
    for i in range(no_of_bdays):
        if i==no_of_bdays-1:
            nex = " "
        elif i==no_of_bdays-2:
            nex = " and "
        elif i<no_of_bdays-2:
            nex = ", "
        p1text+= "<b>"+bdays[i].name+"</b>"+nex

    p1text += "have birthday"+singular+" today. <br> Don't forget to wish!"
    subject = "Birthday"+singular+" Today!"
    global color
    context={ 'title': title,'p1text':p1text,'upcoming_bdays':getupcoming(),'color':color }
    template = get_template('email_wishday.html')
    rendered=template.render(context)
    #f = open("email_temp_gen_text.htm", "w")
    #f.write(rendered)
    #f.close()
    #send_email(subject, message=rendered)
    return subject,rendered


def send_email(subject, message,to=EMAIL_TO,userid=EMAIL_ID,passw=EMAIL_PASSWORD):
    randomstr=str(int(random.random()*1000000))

    msg = email.message.Message()
    msg['Subject'] = subject
    msg['From'] = userid
    msg['To'] = to
    #msg.add_header("Message-ID", myid)
    msg.add_header('Content-Type','text/html')

    msg.add_header('X-Entity-Ref-ID','null')
    msg.set_payload(message)
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(userid,passw)
        server.sendmail(msg['From'], [msg['To']], msg.as_string())
        server.close()
        makeLog("Mail Sent Successful")
        return 0
    except:

        makeLog("Mail not sent, error")
        return 1



def day_to_date(day):
    return datetime.date(datetime.MINYEAR,day.month,day.day)
def date_diff(curr,next):  #only input dates not day
    today=curr
    next_date=next
    if next_date<today:
        next_date = datetime.date(today.year+1,next_date.month,next_date.day)
    return (next_date-today)

class MailerConfig(AppConfig):
    name = 'mailer'
