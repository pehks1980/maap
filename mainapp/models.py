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
    s_time = models.CharField(verbose_name='s_time', max_length=128, blank=True)
    f_time = models.CharField(verbose_name='f_time', max_length=64, blank=True)

    mode = models.CharField(verbose_name='mode', max_length=32, blank=True)

    ans_amount = models.PositiveIntegerField(verbose_name='ans_amount', default=1)  # integer NULL!
    ans_correct = models.PositiveIntegerField(verbose_name='ans_correct', default=0)

    hist = models.TextField(verbose_name='hist', blank=True)

    favor_ans = models.TextField(verbose_name='favor_ans', blank=True)
    wrong_ans = models.TextField(verbose_name='wrong_ans', blank=True)

    qst_time = models.CharField(verbose_name='mode', max_length=64, blank=True)

    a1 = models.PositiveIntegerField(verbose_name='a1', default=0)
    b1 = models.PositiveIntegerField(verbose_name='b1', default=0)
    c1 = models.PositiveIntegerField(verbose_name='c1', default=0)

    #last ans time in seconds
    ans_sum = models.PositiveIntegerField(verbose_name='last_ans_time', default=0)
    #avg ans time for the lesson
    avg_ans_time = models.PositiveIntegerField(verbose_name='avg_ans_time', default=0)
    #settings for questions
    mult = models.PositiveIntegerField(verbose_name='mult', default=1)
    addi = models.PositiveIntegerField(verbose_name='addi', default=1)
    subt = models.PositiveIntegerField(verbose_name='subt', default=1)
    divn = models.PositiveIntegerField(verbose_name='divn', default=1)
    #counter operations for the lesson
    mult_cnt = models.PositiveIntegerField(verbose_name='mult_cnt', default=0)
    addi_cnt = models.PositiveIntegerField(verbose_name='addi_cnt', default=0)
    subt_cnt = models.PositiveIntegerField(verbose_name='subt_cnt', default=0)
    divn_cnt = models.PositiveIntegerField(verbose_name='divn_cnt', default=0)

    def __str__(self):
        return self.user_id







