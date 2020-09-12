from django.shortcuts import render , redirect,HttpResponse
from django.db.models import Q
from django.contrib.auth.models import auth, User ,Group
from .forms import RegisterForm ,HubRegisterForm
from django.contrib import messages
from .models import Day,Month, Ordersummery
from datetime import date
from hub.models import Hub_detail
from delivery.models import Deliveryboy
from client.models import User_data
from django.contrib.auth.decorators import login_required
from milk.decorators import authentication




# Create your views here.
@login_required(login_url='/')
@authentication(allowed='admin')
def dashboard(request):
    dat = str(date.today())
    dat.split('-')
    day = dat[-2:]
    month = dat[-5:-3]
    dataa = Ordersummery.objects.filter(day__date=day, month__m_num=month)
    amount_qry=dataa.values('amount')
    litre_qry = dataa.values('quantity')
    order = dataa.count()
    amount =sum([amt['amount'] for amt in amount_qry])
    quantity = sum([ltr['quantity'] for ltr in litre_qry])
    print(order)
    data = {'orders':dataa, 'amount':amount,'quantity':quantity, 'order':order }

    return render(request, 'dashboard.html', data)


@login_required(login_url='/')
@authentication(allowed='admin')
def newuser(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
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
            return redirect('/dashboard/newuser')
        else:
            print('not valied')
            return redirect('/dashboard/newuser')

    else:
        form = RegisterForm()
        return render(request, 'milk/newuser.html', {'forms': form,'hubs':Hub_detail.objects.all})

@login_required(login_url='/')
@authentication(allowed='admin')
def hubregister(request):
    if request.method == 'POST':
        form = HubRegisterForm(request.POST)
        name = request.POST['hub_name']
        number = request.POST['number']
        address = request.POST['address']
        wnumber = request.POST.get('whatsaap_number')
        if form.is_valid():
            print(name)

            user = form.save()
            grp = Group.objects.get(name = 'Hub')
            user.groups.add(grp)
            sts = Hub_detail(hub_user = user, hub_name = name,number = number,whatsaap_number =wnumber, address=address )
            sts.save()

            return redirect('/dashboard/')

        else:
            return redirect('/hub/register')


    else:
        form = HubRegisterForm()
        # form2 = fullform()
        return render(request, 'milk/newhub.html', {'form':form })



def logout(request):
    auth.logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect('/')

@login_required(login_url='/')
@authentication(allowed='admin')
def search(request):
    input = request.GET.get('search')
    result = User_data.objects.filter(Q(number__icontains = input) | Q(whatsaap_number__icontains=input)).distinct()
    return render(request, 'milk/search.html', {'result': result} )

@login_required(login_url='/')
@authentication(allowed='admin')
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

    return render(request, 'milk/userdetail.html',data )

@login_required(login_url='/')
@authentication(allowed='admin')
def databse(request):
    data = User_data.objects.all().order_by('name')
    dataa={'data':data, }
    return render(request, 'milk/database.html', dataa)



@login_required(login_url='/')
@authentication(allowed='admin')
def membership(request):
    dat = str(date.today())
    dat.split('-')
    day = dat[-2:]
    month = dat[-5:-3]
    member = Ordersummery.objects.filter(month__m_num=month, day__date=day).order_by('month', '-day')
    membr={'mam':member,'months':Month.objects.all, 'days':Day.objects.all}
    return render(request, 'milk/membership.html',membr)


@login_required(login_url='/')
@authentication(allowed='admin')
def hublist(request):
    data = {'hubs':Hub_detail.objects.all}
    return render(request, 'milk/hublist.html',data)



def analytic(request):
    dat = str(date.today())
    dat.split('-')
    day = dat[-2:]
    month = dat[-5:-3]
#todays'data
    dataa = Ordersummery.objects.filter(day__date=day, month__m_num=month)
    amount_qry=dataa.values('amount')
    litre_qry = dataa.values('quantity')
    order = dataa.count()
    amount =sum([amt['amount'] for amt in amount_qry])
    quantity = sum([ltr['quantity'] for ltr in litre_qry])
    Tdataa=Ordersummery.objects.all()
    Tamount_qry=Tdataa.values('amount')
    Tlitre_qry = Tdataa.values('quantity')
    Torder = Tdataa.count()
    Tamount =sum([amt['amount'] for amt in Tamount_qry])
    Tquantity = sum([ltr['quantity'] for ltr in Tlitre_qry])

    data = { 'order':order,'amount':amount,'quantity':quantity , 'torder':Torder, 'tamount':Tamount,'tquantity':Tquantity}

    return render(request, 'milk/anatytic.html',data)

@login_required(login_url='/')
@authentication(allowed='admin')
def hubdetails(request, id):
    hub = Hub_detail.objects.get(id = id)
    dell = Deliveryboy.objects.filter(hub = hub)
    params = {'hub':hub, 'delivery':dell}
    return render(request, 'milk/hubdetails.html',params)

@login_required(login_url='/')
@authentication(allowed='admin')
def filterMonth(request, month):
    filter = Ordersummery.objects.filter(month= month).order_by('month', '-day')
    months = Month.objects.all()
    day = Day.objects.all()
    params={'members':filter,'days':day, 'months':months,'month':month}
    return render(request,'milk/filterBymonth.html', params)

@login_required(login_url='/')
@authentication(allowed='admin')
def filterDay(request, month,day):
     filter = Ordersummery.objects.filter(month = month,day=day).order_by('-day')
     months = Month.objects.all()
     days = Day.objects.all()
     params = {'months':months, 'day':day, 'days':days,'members':filter,'month':month}
     return render(request, 'milk/filterByDay.html', params)


@login_required(login_url='/')
@authentication(allowed='admin')
def orderupdate(request,id):
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

    return render(request, 'client/orderUpdate2.html', {'order':ordr,'months':Month.objects.all,'days':Day.objects.all})

@login_required(login_url='/')
@authentication(allowed='admin')
def orderdelete(request,id,uid):
    ordr = Ordersummery.objects.get(id= id)
    ordr.delete()
    return redirect('/dashboard/user/'+str(uid))







