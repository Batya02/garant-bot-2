from os import truncate
from django.db import models

from datetime import datetime as dt

class AuthUser(models.Model):

    id = models.IntegerField(primary_key=True)
    password = models.CharField(max_length=128)
    user_id = models.IntegerField()
    is_superuser = models.BooleanField(default=False)
    username = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(max_length=255, default=None)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=dt.now())
    first_name = models.CharField(max_length=150)
    balance = models.FloatField(default=0.0)

    def __str__(self):
        return "<AuthUser %i %s %i %r %s %s %s %r %r %s %s %.2f>" % (
            self.id, self.password, self.user_id, self.is_superuser,
            self.username, self.last_name, self.email, self.is_staff,
            self.is_active, self.date_joined, self.first_name, self.balance,)

class ShopsAndSales(models.Model):

    id = models.IntegerField(primary_key=True)
    main_user = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    uncreated = models.DateTimeField()
    price = models.FloatField()
    not_main_user = models.IntegerField()
    type = models.CharField(max_length=4)
    ended = models.BooleanField()

    def __str__(self):
        return "<ShopsAndSales %i %i %s %s %.2f %i %s %r>" % (
            self.id, self.main_user, 
            dt.strftime(self.created, "%Y-%m-%d %H:%M:%S"),
            dt.strftime(self.uncreated, "%Y-%m-%d %H:%M:%S"),
            self.price, self.not_main_user, 
            self.type, self.ended,)

class OutputApplication(models.Model):
    
    id = models.IntegerField(primary_key=True)
    user_id = models.IntegerField()
    amount = models.FloatField()
    created = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField()

    def __str__(self):
        return "<OutputApplication %i %i %.2f %s %r>" % (
            self.id, self.user_id,
            self.amount, self.created, 
            self.status,)