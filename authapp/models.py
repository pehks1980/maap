from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser

from django.db.models.signals import post_save
from django.dispatch import receiver

class MaapUser(AbstractUser):
    avatar = models.ImageField(upload_to='users_avatars', blank=True)
    age = models.PositiveIntegerField(verbose_name = 'age', blank=True)


    def __str__(self):
        return self.name

#class for additional info stored in this user profile
class MaapUserProfile(models.Model):

    APP_EMAIL_CHOICES = (
        (3, 'Раз в 3 дня'),
        (7, 'Раз в неделю'),

    )

    user = models.OneToOneField(MaapUser, unique=True, null=False, db_index=True, on_delete=models.CASCADE)
    email_addr = models.CharField(verbose_name='Ваш E-MAIL:', max_length=64, blank=True)
    email_shed = models.PositiveIntegerField(verbose_name='Режим оповещения', choices=APP_EMAIL_CHOICES, blank=True , null=True)
    created_at = models.DateTimeField(auto_now_add=True)  # time when it started
    last_fired_at = models.DateTimeField(auto_now_add=True, blank=True)
    enabled = models.BooleanField(default=True)

    @receiver(post_save, sender=MaapUser)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            MaapUserProfile.objects.create(user=instance)

    @receiver(post_save, sender=MaapUser)
    def save_user_profile(sender, instance, **kwargs):
        instance.maapuserprofile.save()




