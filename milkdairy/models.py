from django.db import models
from datetime import date

# Create your models here.
class Hubs(models.Model):
    id = models.AutoField
    hub_name = models.CharField(max_length=100)
    address = models.CharField(max_length= 200)
    hub_number = models.IntegerField()

    def __str__(self):
        return self.hub_name

class Orders(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    num = models.IntegerField()
    date = models.DateField(("Date"),default=date.today)
    hub_id = models.ForeignKey(Hubs, default=1,on_delete=models.SET_DEFAULT)
    quantity = models.DecimalField(max_digits=9999, decimal_places=2)
    amount = models.IntegerField()

    def __str__(self):
        return self.name


class Members(models.Model):
    id = models.AutoField
    order_id = models.ForeignKey(Orders, default=1, on_delete=models.SET_DEFAULT)
    #starting = models.DateField(("Date"),default=date.today)
    #ending = models.DateField()
    membership = models.CharField(max_length=10,default='Yes')
    #month_id =models.ManyToManyField('Month', blank=True)



class Month(models.Model):
    id =models.AutoField(primary_key=True)

    months = models.CharField(max_length=20,)

    year = models.CharField(max_length=5,default='2020')

    def __str__(self):
        return self.months



class Day (models.Model):
    id = models.AutoField(primary_key=True)
    date = models.CharField(max_length=3)
   # members_id = models.ManyToManyField(Members, blank=True)
    #month_id = models.ForeignKey(Month,default=1, on_delete=models.SET_DEFAULT)
    #next_month_id = models.IntegerField(blank=True,null=True,)
    #next_day = models.IntegerField(blank=True,null=True)
    #next_year = models.CharField(max_length=5,blank=True,null=True)

    def __str__(self):
        return self.date




class daysrel(models.Model):
    id = models.AutoField(primary_key = True)
    user_id = models.ForeignKey(Members,null=True, blank=True, on_delete=models.SET_NULL)
    month_id = models.ForeignKey(Month,blank=True, null=True,on_delete=models.SET_NULL)
    day_id = models.ManyToManyField(Day, blank=True,)



