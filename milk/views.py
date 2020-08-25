from django.shortcuts import render,redirect, HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

def index(request):
    return render(request, 'index.html')

def login(request):
    if request.user.is_authenticated:
        print('yes')
        return redirect('/dashboard')
    else:
        if request.method =='POST':
            uame = request.POST['uname']
            pname = request.POST['pas']
            user = auth.authenticate(username=uame ,password = pname)
            if user is not None:
                auth.login(request, user)
                return redirect('/dashboard')
            else:
                return redirect('/')
        else:
             return redirect('')



