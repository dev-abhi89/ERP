from django.shortcuts import render,redirect, HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User, auth
from .decorators import auth as uauth

# Create your views here.

def index(request):
    return render(request, 'index.html')

@uauth
def login(request):
    group = None

    if request.method =='POST':
        uame = request.POST['uname']
        pname = request.POST['pas']
        user = auth.authenticate(username=uame ,password = pname)
        if user is not None:
            print('right')
            auth.login(request, user)

            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
                if group == 'Hub':
                    return redirect('/hub/home')
                if group == 'delivery':
                    return redirect('/delivery/')
                if group == 'client':
                    return redirect('/user/')
                if group == 'admin':
                    return redirect('/dashboard/')
            return HttpResponse('unable to find group')
        else:
            print('wrong')
            return redirect('/')

    return render(request, 'index.html')



