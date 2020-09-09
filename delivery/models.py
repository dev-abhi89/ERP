from django.db import models
from django.contrib.auth.models import User
# Create your models here.



class Deliveryboy(models.Model):
    id = models.AutoField(primary_key=True)
    users = models.OneToOneField(User, on_delete=models.CASCADE)
    details = models.CharField(max_length=225, blank=True, null=True)
    name = models.CharField(max_length=225)
    number = models.IntegerField( default=00000000)
    address = models.CharField(max_length=400, default='default_address')
    whatsaap_number = models.IntegerField(default = 0000000000)
    hub = models.ForeignKey('hub.Hub_detail', blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name
