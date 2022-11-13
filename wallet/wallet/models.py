from enum import unique
from pyexpat import model
from django.db import models
import datetime
from django.contrib.auth.models import Permission, User
from django.core.validators import RegexValidator
from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator


class Owner(models.Model):
    user_id = models.OneToOneField(User, default=1,on_delete=models.CASCADE, unique=True)
    user_name = models.CharField(unique=True)
    balance = models.PositiveIntegerField(default=50)
    date = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-date"]


class Balance(models.Model):
    user = models.ForeignKey(User, default=1,on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(default=0)


class Transfer(models.Model):
    username = models.ForeignKey(User, default=1,on_delete=models.CASCADE)
    transfer_amount = models.PositiveIntegerField(default=10, validators=[MaxValueValidator(5000),MinValueValidator(10)])
    date = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return str(self.transfer_amount)

    class Meta:
        ordering = ["-date"]


class ReceivedAmount(models.Model):
    username = models.ForeignKey(User, default=1,on_delete=models.CASCADE)
    rec_name = models.CharField(max_length=30)
    rec_amount = models.PositiveIntegerField(default=100, validators=[MaxValueValidator(5000)])
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return str(self.rec_amount)

    class Meta:
        ordering = ["-timestamp"]