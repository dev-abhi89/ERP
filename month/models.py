from django.db import models


# Create your models here.
class January(models.Model):
    id = models.AutoField(primary_key=True)
    days = models.CharField(max_length = 50)
    member_id= models.ManyToManyField('milkdairy.Orders')

