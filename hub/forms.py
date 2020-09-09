from django import forms
from django.contrib.auth.forms import UserCreationForm ,forms as fm
from django.contrib.auth.models import User , Group



class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    number = forms.IntegerField()
    wnumber = forms.IntegerField()
    class Meta:
        model = User
        fields = ["username","first_name","last_name" , "email", "password1", "password2"]
    # class Meta(Meta):
    #     model = Deliveryboy
    #     fields = ['users', 'number' , 'address']

# class fullform(fm.ModelForm):
#     class Meta:
#         model = Deliveryboy
#         fields = ['users', 'number' , 'address']
