from django.db import models
from datetime import date






class Month(models.Model):
    id =models.AutoField(primary_key=True)
    months = models.CharField(max_length=20,)
    m_num = models.CharField( max_length=3,blank=True,null=True)
    year = models.CharField(max_length=5,default='2020')
    def __str__(self):
        return self.months



class Day (models.Model):
    id = models.AutoField(primary_key=True)
    date = models.CharField(max_length=3)
    def __str__(self):
        return self.date








class Ordersummery(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('client.User_data',default=1, on_delete=models.SET_DEFAULT)
    month = models.ForeignKey(Month, on_delete=models.CASCADE)
    day = models.ForeignKey(Day, on_delete=models.CASCADE)
    amount = models.IntegerField()
    quantity = models.DecimalField(max_digits=99999,decimal_places=2)
    status = models.CharField(max_length=20, default='in transit')
    payment = models.CharField(max_length=20, default='unpaid')
    date= models.DateTimeField(auto_now_add=True)
    hub = models.ForeignKey('hub.Hub_detail',null=True, on_delete=models.SET_NULL)
    delivery = models.ForeignKey('delivery.Deliveryboy', blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.status
