from django.db import models
from django.contrib.auth.models import  User

# class Hub(AbstractUser):
#     email = models.EmailField(max_length=225, unique=True,default='default@blank.com')
#     full_name = models.CharField(max_length=225, blank = True,null=True)
#     active = models.BooleanField(default=False)
#     staff = models.BooleanField(default=True)
#     superuser = models.BooleanField(default=False)
#     _group = EmptyManager(Group)
#     _user_permissions = EmptyManager(PermissionsMixin)
#
#     def __str__(self):
#         return self.email
#     @property
#     def is_active(self):
#         return self.active
#     @property
#     def is_staff(self):
#         return self.staff
#     @property
#     def is_superuser(self):
#         return self.superuser
#
#     @property
#     def groups(self):
#         return self._groups
#     @property
#     def user_permissions(self):
#         return self._user_permissions
#
#
#
#



# Create your models here.


class Deliveryboy(models.Model):
    users = models.OneToOneField(User, on_delete=models.CASCADE)
    details = models.CharField(max_length=225, blank=True, null=True)
    name = models.CharField(max_length=225)
    number = models.IntegerField( default=00000000)
    address = models.CharField(max_length=400, default='default_address')
    whatsaap_number = models.IntegerField(default = 0000000000)

    def __str__(self):
        return self.name
