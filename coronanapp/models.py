from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Bet(models.Model):
    moneyBet = models.IntegerField(blank=True, null=True)
    moneyWon = models.IntegerField(blank=True, null=True)
    ratio = models.IntegerField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    cases = models.IntegerField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    funds = models.IntegerField(blank=True, null=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()