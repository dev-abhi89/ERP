from django.shortcuts import render ,redirect , HttpResponse

# Create your views here.
from .forms import  RegisterForm
from .models import  Deliveryboy
from django.contrib.auth.models import Group

from .forms import RegisterForm

from milkdairy.models import Orders,daysrel
from datetime import date
# Create your views here.
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        name = request.POST['first_name'] + ' ' + request.POST['last_name']
        if form.is_valid():
            print(name)

            user = form.save()
            grp = Group.objects.get(name = 'delivery')
            user.groups.add(grp)
            sts = Deliveryboy(users = user, name = name )
            sts.save()

            return redirect('/hub/login')

        else:
             return redirect('/hub/register')


    else:
        form = RegisterForm()
        return render(request, 'hub/register.html', {'form':form})


def login(request):
    return redirect('/hub/home')

def index(request):
    dat = str(date.today())
    dat.split('-')

    day = dat[-2:]
    month = dat[-4:-3]
    data = daysrel.objects.filter(day_id = day, month_id =month)
    return render(request, 'hub/home.html', {'test':Orders.objects.all,'filter':data})
