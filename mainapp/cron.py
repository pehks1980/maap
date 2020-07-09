from datetime import datetime

from django.utils.timezone import make_aware

from django_cron import CronJobBase, Schedule

from _mailsend import mail_notify

from authapp.models import MaapUserProfile

#there is need to pip install django_cron and update users crontab
# crontab -e
# put this
# SHELL=/bin/bash
# */1 * * * * source /home/user/.bashrc && source /home/user/django/venv/bin/activate && python /home/user/django/maap/manage.py runcrons >> /home/user/django/maap/cronjob.log 2>&1
#also need to install in system local post MTA like postfix

def cron_notify(jobs,dont_wait=False):
    print(f' {datetime.now()}: Hello from cron')

    for job in jobs:
        if job.enabled == True:
            # check the time to fire
            # if job.last_fired_at == None:
            #     diff_time = datetime.now() - job.created_at.replace(tzinfo=None)
            # else:
            #     diff_time = datetime.now() - job.last_fired_at.replace(tzinfo=None)

            if job.last_fired_at == None:
                diff_time = make_aware(datetime.now()) - job.created_at
            else:
                diff_time = make_aware(datetime.now()) - job.last_fired_at


            diff_time_mins = int(diff_time.total_seconds() / 60)

            time_period = job.email_shed * 1440

            if dont_wait == True:
                diff_time_mins = 100000

            if diff_time_mins > time_period:
                # to set new peroid, send mail
                # we need to send mail
                #job.last_fired_at = datetime.now()
                job.last_fired_at = make_aware(datetime.now())
                job.save()
                # print send_mail
                user = {'first_name' : job.user.first_name,
                        'last_name' : job.user.last_name,
                        'id' : job.user.id,
                        'rem_period' : job.email_shed,
                        }

                mail_notify(job.email_addr, user=user)

    print(f' {datetime.now()}: Bye from cron')

class MyCronJob(CronJobBase):
    RUN_EVERY_MINS = 5 # every 2 hours
    #1440*3 3days
    #1440*7 7days
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'maap.my_cron_job'    # a unique code

    def do(self):
        print('cron_notify executed..')
        jobs = MaapUserProfile.objects.all()
        cron_notify(jobs)
