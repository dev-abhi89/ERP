from django.contrib import admin

# Register your models here.
from .models import Members, Orders, Hubs,Month,Day,daysrel
admin.site.register(Members)
admin.site.register(Orders)
admin.site.register(Hubs)
admin.site.register(Month)
admin.site.register(Day)
admin.site.register(daysrel)


