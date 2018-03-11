from django.db import models
import datetime

class Item(models.Model):
    text = models.TextField(default='')
    my_date = models.DateField()

