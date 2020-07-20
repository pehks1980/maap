import collections
import random

from django.db import models

from django.conf import settings

# Create your models here.

import random, collections, time, threading

from datetime import datetime

import random

class Report(models.Model):
    bytes = models.TextField()
    filename = models.CharField(max_length=255)
    mimetype = models.CharField(max_length=50)

class MaapReport(models.Model):
   # report_pk = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    file_rep = models.FileField(
        upload_to='mainapp.Report/bytes/filename/mimetype',
        blank=True, null=True
    )

    def __str__(self):
        return self.name


class MaapLesson(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='lesson')
    report = models.ForeignKey(MaapReport, on_delete=models.CASCADE)

    date = models.CharField(verbose_name='s_time', max_length=64, blank=True)
    s_time = models.CharField(verbose_name='s_time', max_length=64, blank=True)
    f_time = models.CharField(verbose_name='f_time', max_length=64, blank=True)
    # mode=models.PositiveIntegerField(verbose_name='mode', null=True)
    mode = models.CharField(verbose_name='mode', max_length=12, blank=True)

    ans_amount = models.PositiveIntegerField(verbose_name='ans_amount', default=1)  # integer NULL!
    ans_correct = models.PositiveIntegerField(verbose_name='ans_correct', default=0)

    nx = models.PositiveIntegerField(verbose_name='nx', default=12)
    ny = models.PositiveIntegerField(verbose_name='ny', default=10)

    ax = models.PositiveIntegerField(verbose_name='ax', default=50)
    sx = models.PositiveIntegerField(verbose_name='sx', default=50)

    two_digit = models.PositiveIntegerField(verbose_name='two_digit', default=1)
    no_minus = models.PositiveIntegerField(verbose_name='no_minus', default=1)
    no_dec_mul = models.PositiveIntegerField(verbose_name='no_dec_mul', default=1)

    hist_depth = models.PositiveIntegerField(verbose_name='hist_depth', default=5)
    favor_thresold_time = models.PositiveIntegerField(verbose_name='hist_depth', default=15)

    hist = models.CharField(verbose_name='hist', max_length=256, blank=True)
    favor_ans = models.CharField(verbose_name='hist', max_length=256, blank=True)

    qst_time = models.CharField(verbose_name='mode', max_length=12, blank=True)

    mult = models.PositiveIntegerField(verbose_name='mult', default=1)
    addi = models.PositiveIntegerField(verbose_name='addi', default=1)
    subt = models.PositiveIntegerField(verbose_name='subt', default=1)

    a1 = models.PositiveIntegerField(verbose_name='a1', default=0)
    b1 = models.PositiveIntegerField(verbose_name='b1', default=0)
    c1 = models.PositiveIntegerField(verbose_name='c1', default=0)

    #last ans time in seconds
    ans_sum = models.PositiveIntegerField(verbose_name='last_ans_time', default=0)
    #avg ans time for the lesson
    avg_ans_time = models.PositiveIntegerField(verbose_name='avg_ans_time', default=0)
    #mult_tabl =


    def __str__(self):
        return self.user_id







