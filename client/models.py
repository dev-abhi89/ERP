from django.db import models

# Create your models here.
from django.contrib.auth.models import User


class User_data(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=225)
    number = models.IntegerField()
    whatsaap_number = models.IntegerField()
    address = models.CharField(max_length=400)
    date = models.DateField(auto_now_add=True)
    hub = models.ForeignKey('hub.Hub_detail' ,null=True,blank=True , on_delete=models.SET_NULL)

    def __str__(self):
        return self.name
