from django.db import models

class User(models.Model):
    token = models.CharField(max_length=200)
