from django.contrib import admin

# Register your models here.
from .models import Month,Day, Ordersummery

admin.site.register(Month)
admin.site.register(Day)
admin.site.register(Ordersummery)



