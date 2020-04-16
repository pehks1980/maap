from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser


class MaapUser(AbstractUser):
    avatar = models.ImageField(upload_to='users_avatars', blank=True)
    age = models.PositiveIntegerField(verbose_name = 'age', blank=True)


    def __str__(self):
        return self.name


