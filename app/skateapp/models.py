from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import User as AuthUser

class Competition(models.Model):
    city = models.CharField(max_length=45)
    street = models.CharField(max_length=45)
    date = models.DateField()
    description = models.CharField(max_length=255)

class User(models.Model):

    class GenderUser(models.TextChoices):
        Kobieta = "K"
        Mezczyzna = "M"

    class StanceUser(models.TextChoices):
        Goofy = "G"
        Regular = "R"

    age = models.IntegerField()
    gender = models.CharField(max_length=1, choices=GenderUser.choices)
    stance = models.CharField(max_length=1, choices=StanceUser.choices)
    user = models.OneToOneField(AuthUser, on_delete=models.CASCADE, null=True)

class Registration(models.Model):

    class RegistrationStatus(models.TextChoices):
        Oczekujace = 'SEND'
        Zaakceptowane = 'OK'
        Odrzucone = 'NOT'

    status = models.CharField(max_length=4, choices=RegistrationStatus.choices, default=RegistrationStatus.Oczekujace)
    id_competition = models.ForeignKey(Competition, related_name='registration', null=False, blank=False, on_delete=models.DO_NOTHING)
    id_user = models.ForeignKey(AuthUser, related_name='registration', null=False, blank=False, on_delete=models.DO_NOTHING)