from django.shortcuts import render ,redirect , HttpResponse
from django.contrib.auth import authenticate
from .models import Hub_detail
from milk.decorators import authentication
from django.contrib.auth.decorators import login_required

# Create your views here.
from milkdairy.models import Ordersummery
from delivery.models import  Deliveryboy
from django.contrib.auth.models import Group

from .forms import RegisterForm


from datetime import date
# Create your views here.
@login_required(login_url='/')
@authentication(allowed='Hub')
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        name = request.POST['first_name'] + ' ' + request.POST['last_name']
        number = request.POST['number']
        wnumber = request.POST['wnumber']

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
        # form2 = fullform()
        return render(request, 'hub/register.html', {'form':form })




@login_required(login_url='/')
def login(request):
    return redirect('/hub/home')
@login_required(login_url='/')
@authentication(allowed='Hub')
def index(request):
    dat = str(date.today())
    dat.split('-')
    day = dat[-1:]
    month = dat[-4:-3]
    user =Hub_detail.objects.get(hub_user =request.user)
    print(user)

    data = Ordersummery.objects.filter(hub=user, day_id = day, month_id =month)
    print(data)
    if request.method =='POST':
        deliveryboy_id = request.POST['delivery']
        order_id = request.POST.get('ordr')
        print(order_id)
        order = Ordersummery.objects.get(id=order_id)
        deliveryboy = Deliveryboy.objects.get(id = deliveryboy_id)
        order.delivery = deliveryboy
        order.save()
    return render(request, 'hub/home.html', {'filter':data, 'delivery':Deliveryboy.objects.all})
@login_required(login_url='/')
@authentication(allowed='Hub')
def profile(request):
    if request.user.is_authenticated:
        user =request.user
        hub = Hub_detail.objects.get(hub_user = user)
        print(hub)
        return render(request, 'hub/profile.html', {'hub':hub} )

    else:
        redirect('/hub/login')
@login_required(login_url='/')
@authentication(allowed='Hub')
def undefined(request):
    user =Hub_detail.objects.get(hub_user =request.user)
    data = Ordersummery.objects.filter(hub=user)





