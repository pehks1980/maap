from django.db import models

from django.conf import settings

# Create your models here.

class MaapLesson(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='lesson')

    date = models.CharField(verbose_name='s_time', max_length=24, blank=True)
    s_time = models.CharField(verbose_name='s_time', max_length=12, blank=True)
    f_time = models.CharField(verbose_name='f_time', max_length=12, blank=True)
    #mode=models.PositiveIntegerField(verbose_name='mode', null=True)
    mode = models.CharField(verbose_name='mode', max_length=12, blank=True)
    ans_amount = models.PositiveIntegerField(verbose_name='ans_amount', null=True)#integer NULL!
    ans_correct = models.PositiveIntegerField(verbose_name='ans_correct', null=True)

    def __str__(self):
        return self.name