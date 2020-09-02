from django.db import models

# Create your models here.
class Status(models.Model):
    delivery_boy = models.ForeignKey('hub.Deliveryboy' , on_delete=models.CASCADE)
    order = models.ForeignKey('milkdairy.daysrel', on_delete=models.CASCADE)
    s_choice = (('undelivered','undelivered'), ('out for delivery', 'out for delivery'), ('delivered', 'delivered'))
    status = models.CharField(choices=s_choice,max_length=50 , default='undelivered')
