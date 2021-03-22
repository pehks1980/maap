from datetime import datetime

from django.utils.timezone import make_aware

from django_cron import CronJobBase, Schedule

from _mailsend import mail_notify

from authapp.models import MaapUserProfile


# there is need to pip install django_cron and update
# users crontab crontab -e put this SHELL=/bin/bash */1 * * * *
# source /home/user/.bashrc && source
# /home/user/django/venv/bin/activate && python /home/user/django/maap/manage.py
# runcrons >> /home/user/django/maap/cronjob.log 2>&1 also need to
# install in system local post MTA like postfix

def cron_notify(jobs, dont_wait=False):
    """
    cron notify by email
    :param jobs:
    :param dont_wait:
    :return:
    """
    print(f' {datetime.now()}: Hello from cron')

    for job in jobs:
        if job.enabled:
            # check the time to fire
            # if job.last_fired_at == None:
            #     diff_time = datetime.now() - job.created_at.replace(tzinfo=None)
            # else:
            #     diff_time = datetime.now() - job.last_fired_at.replace(tzinfo=None)

            if job.last_fired_at is None:
                diff_time = make_aware(datetime.now()) - job.created_at
            else:
                diff_time = make_aware(datetime.now()) - job.last_fired_at

            diff_time_mins = int(diff_time.total_seconds() / 60)

            try:
                time_period = job.email_shed * 1440
                print(
                    f' job for user id = {job.user.id} ({job.email_addr}) has {job.email_shed} param which means time period : {time_period} (mins) last time fired : {job.last_fired_at} difference : {diff_time_mins} (mins)')
            except:
                print(f' job = {job.user.id} has {job.email_shed} parameter will not fire notification')
                time_period = 0
                diff_time_mins = -1

            if dont_wait:
                diff_time_mins = 100000

            if diff_time_mins > time_period:
                # to set new peroid, send mail
                # we need to send mail
                # job.last_fired_at = datetime.now()
                job.last_fired_at = make_aware(datetime.now())
                job.save()
                # print send_mail
                user = {'first_name': job.user.first_name,
                        'last_name': job.user.last_name,
                        'id': job.user.id,
                        'rem_period': job.email_shed,
                        }

                mail_notify(job.email_addr, user=user)

    print(f' {datetime.now()}: Bye from cron')


class MyCronJob(CronJobBase):
    """
    class for cronjob as per pip lib
    """
    RUN_EVERY_MINS = 6 * 60  # every 2 hours
    # 1440*3 3days
    # 1440*7 7days
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'maap.my_cron_job'  # a unique code

    def do(self):
        """
        execute when scheduled event happened
        :return:
        """
        print('cron_notify executed..')
        jobs = MaapUserProfile.objects.all()
        cron_notify(jobs)
