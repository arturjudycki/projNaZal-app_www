from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import User as AuthUser

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

class Competition(models.Model):
    city = models.CharField(max_length=45)
    street = models.CharField(max_length=45)
    date = models.DateField()
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.city + ", " + self.street

class User_detail(models.Model):

    class GenderUser(models.TextChoices):
        Kobieta = "K"
        Mężczyzna = "M"

    class StanceUser(models.TextChoices):
        Goofy = "Goofy"
        Regular = "Regular"

    age = models.IntegerField(null=True)
    gender = models.CharField(max_length=1, choices=GenderUser.choices, null=True)
    stance = models.CharField(max_length=7, choices=StanceUser.choices, null=True)
    user = models.OneToOneField(AuthUser, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name

class Registration(models.Model):

    class RegistrationStatus(models.TextChoices):
        Oczekujace = 'SEND'
        Zaakceptowane = 'OK'
        Odrzucone = 'NOT'

    status = models.CharField(max_length=4, choices=RegistrationStatus.choices, default=RegistrationStatus.Oczekujace)
    id_competition = models.ForeignKey(Competition, related_name='registration', null=True, blank=True, on_delete=models.DO_NOTHING)
    id_user = models.ForeignKey(AuthUser, related_name='registration', null=True, blank=True, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.status + ", " + self.id_competition.city + ", " + self.id_user.first_name + " " + self.id_user.last_name

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)