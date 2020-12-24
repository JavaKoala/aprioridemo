from django.db import models

# Create your models here.
class DataSet(models.Model):
    datafile = models.FileField(upload_to='datafiles/%Y/%m/%d')