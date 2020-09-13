from django.shortcuts import render ,redirect , HttpResponse
from .models import Hub_detail
from milk.decorators import authentication
from django.contrib.auth.decorators import login_required

# Create your views here.
from milkdairy.models import Ordersummery, Month, Day
from delivery.models import  Deliveryboy
from django.contrib.auth.models import Group
from client.models import  User_data
from .forms import RegisterForm
from django.db.models import Q
from milkdairy.forms import RegisterForm as rform

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
        address = request.POST['address']

        if form.is_valid():
            print(name)

            user = form.save()
            grp = Group.objects.get(name = 'delivery')
            user.groups.add(grp)
            hub = Hub_detail.objects.get(hub_user=request.user)
            sts = Deliveryboy(users = user, name = name,hub=hub,address=address, number=number, whatsaap_number =wnumber, )
            sts.save()

            return redirect('/hub/login')

        else:
             return redirect('/hub/register')


    else:
        form = RegisterForm()
        # form2 = fullform()
        return render(request, 'hub/register.html', {'form':form })
@login_required(login_url='/')
@authentication(allowed='Hub')
def newuser(request):
    if request.method == 'POST':
        form = rform(request.POST)
        name = request.POST['first_name'] + ' ' + request.POST['last_name']
        number = request.POST['number']
        address = request.POST['address']
        wnumber = request.POST.get('whatsaa_number')
        hub_id = request.POST.get('hubs')
        hub = Hub_detail.objects.get(id = hub_id)
        if form.is_valid():
            user  = form.save()
            grp = Group.objects.get(name = 'client')
            user.groups.add(grp)
            entry = User_data(user_id = user,hub = hub ,name = name, number = number, address=address, whatsaap_number=wnumber)
            entry.save()
            print([name, number, address, wnumber])
            return redirect('/hub/newuser')
        else:
            print('not valied')
            return redirect('/hub/newuser')

    else:
        form = rform()
        return render(request, 'hub/newuser.html', {'forms': form,'hubs':Hub_detail.objects.all})




@login_required(login_url='/')
def login(request):
    return redirect('/hub/home')
@login_required(login_url='/')
@authentication(allowed='Hub')
def index(request):
    dat = str(date.today())
    dat.split('-')
    day = dat[-2:]
    month = dat[-5:-3]
    user =Hub_detail.objects.get(hub_user =request.user)
    print(user)

    data = Ordersummery.objects.filter(hub=user, day__date = day, month__m_num =month)
    dlvrd = data.filter(status='delivered').count()
    uncnfrmd = data.filter(delivery=None).count()
    trnsit = data.filter(status='out for delivery').count()
    print(trnsit)
    if request.method =='POST':
        deliveryboy_id = request.POST['delivery']
        order_id = request.POST.get('ordr')
        print(order_id)
        order = Ordersummery.objects.get(id=order_id)
        deliveryboy = Deliveryboy.objects.get(id = deliveryboy_id)
        order.delivery = deliveryboy
        order.save()
    return render(request, 'hub/home.html', {'filter':data,'delivered':dlvrd,'trnsit':trnsit,'unconfirmed':uncnfrmd ,'delivery':Deliveryboy.objects.all})
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
    hub = Hub_detail.objects.get(hub_user=request.user)
    data = Ordersummery.objects.filter(user__hub=hub,delivery=None)
    dell = Deliveryboy.objects.filter(hub = hub)
    if request.method == 'POST':
        ordr_id = request.POST.get('oid')
        del_id = request.POST.get('delivery')
        order = Ordersummery.objects.get(id=ordr_id)
        delivery= Deliveryboy.objects.get(id=del_id)
        order.delivery = delivery
        order.save()
        return redirect('/hub/un-confirmed')
    return render(request,'hub/undefined.html', {'orders':data,'delivery':dell})


@login_required(login_url='/')
@authentication(allowed='Hub')
def search(request):
    input = request.GET.get('search')
    result = User_data.objects.filter(Q(number__icontains = input) | Q(whatsaap_number__icontains=input)).distinct()
    return render(request, 'hub/search.html', {'result': result} )

@login_required(login_url='/')
@authentication(allowed='Hub')
def userdetail(request, id):
    user = User_data.objects.get(id=id)
    orders = Ordersummery.objects.filter(user =user).order_by('month', 'day')
    data = {'user':user, 'months':Month.objects.all, 'days':Day.objects.all,'order':orders}
    if request.method =='POST':
        amount = request.POST['amount']
        quantity = request.POST['quantity']
        month_id = request.POST['months']
        month = Month.objects.get(id = month_id)
        day_id = request.POST.getlist('days')
        hub = user.hub
        #print(hub)
        for day in day_id:
            daydata = Day.objects.get(id = day)
            entry = Ordersummery(user = user,hub = hub, month =month, day = daydata, amount = amount, quantity=quantity)
            entry.save()
            #print(entry)




    return render(request, 'hub/userdetail.html',data )


@login_required(login_url='/')
@authentication(allowed='Hub')
def databse(request):
    hub = Hub_detail.objects.get(hub_user=request.user)
    data = User_data.objects.filter(hub=hub).order_by('name')
    dataa={'data':data, }
    return render(request, 'hub/database.html', dataa)



@login_required(login_url='/')
@authentication(allowed='Hub')
def membership(request):
    dat = str(date.today())
    dat.split('-')
    day = dat[-2:]
    month = dat[-5:-3]
    hub = Hub_detail.objects.get(hub_user=request.user)
    member = Ordersummery.objects.filter(hub = hub,month__m_num=month, day__date=day).order_by('month', '-day')



    membr={'mam':member,'months':Month.objects.all, 'days':Day.objects.all}
    return render(request, 'hub/membership.html',membr)




@login_required(login_url='/')
@authentication(allowed='Hub')
def filterMonth(request, month):
    hub = Hub_detail.objects.get(hub_user=request.user)
    filter = Ordersummery.objects.filter(hub =hub,month= month).order_by('month', '-day')
    months = Month.objects.all()
    day = Day.objects.all()
    params={'members':filter,'days':day, 'months':months,'month':month}

    return render(request,'hub/filterBymonth.html', params)

@login_required(login_url='/')
@authentication(allowed='Hub')
def filterDay(request, month,day):
     hub = Hub_detail.objects.get(hub_user=request.user)
     filter = Ordersummery.objects.filter(hub =hub,month = month,day=day).order_by('-day')
     months = Month.objects.all()
     days = Day.objects.all()
     params = {'months':months, 'day':day, 'days':days,'members':filter,'month':month}
     return render(request, 'hub/filterByDay.html', params)


@login_required(login_url='/')
@authentication(allowed='Hub')
def orderupdate(request,id):
   # user = User_data.objects.get(user_id = request.user)
    ordr = Ordersummery.objects.get(id= id)
    if request.method == 'POST':
        amnt = request.POST.get('amount')
        quantity = request.POST.get('quantity')
        month_id = request.POST.get('month')
        month = Month.objects.get(id=month_id)
        day_id = request.POST.get('day')
        day = Day.objects.get(id=day_id)
        ordr.month =month
        ordr.day =day
        ordr.amount = amnt
        ordr.quantity = quantity
        ordr.save()

    return render(request, 'hub/orderUpdate2.html', {'order':ordr,'months':Month.objects.all,'days':Day.objects.all})

@login_required(login_url='/')
@authentication(allowed='Hub')
def orderdelete(request,id,uid):
   # user = User_data.objects.get(user_id = request.user)
    ordr = Ordersummery.objects.get(id= id)
    ordr.delete()
    return redirect('/hub/user/'+str(uid))

def deliverylist(request):
    hub =Hub_detail.objects.get(hub_user =request.user)
    boys = Deliveryboy.objects.filter(hub=hub)
    return render(request, 'hub/deliverylist.html', {'list':boys})

def deliverydetail(request, id):
    hub =Hub_detail.objects.get(hub_user =request.user)
    data = Deliveryboy.objects.get(id=id, hub=hub)
    return render(request, 'hub/deliverydetails.html', {'user':data})


def profileupdate(request):
    user = Hub_detail.objects.get(hub_user = request.user)
    if request.method == 'POST':
        name = request.POST.get('name')
        number = request.POST.get('number')
        wnumber =request.POST.get('wnumber')
        addres = request.POST.get('address')

        user.name=name
        user.number=number
        user.whatsaap_number=wnumber
        user.address=addres
        user.save()





    return render(request, 'hub/update.html',{'user':user})



