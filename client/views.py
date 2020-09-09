from django.shortcuts import render, redirect
from .models import User_data
from milkdairy.models import Ordersummery,Month,Day
from datetime import date
from milk.decorators import authentication
from django.contrib.auth.decorators import login_required



# Create your views here.
@login_required(login_url='/')
@authentication(allowed='client')
def home(request):
    user = User_data.objects.get(user_id = request.user)
    dat = str(date.today())
    dat.split('-')
    day = dat[-1:]
    month = dat[-4:-3]
    ordr = Ordersummery.objects.filter(user=user, day_id = day, month_id =month)
    return render(request, 'client/index.html', {'user':user, 'order':ordr})
@login_required(login_url='/')
@authentication(allowed='client')
def profile(request):
    user = User_data.objects.get(user_id = request.user)

    return render(request, 'client/profile.html', {'user':user})
@login_required(login_url='/')
@authentication(allowed='client')
def update(request):
    user = User_data.objects.get(user_id = request.user)
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





    return render(request, 'client/update.html',{'user':user})
@login_required(login_url='/')
@authentication(allowed='client')
def order(request):
    user = User_data.objects.get(user_id = request.user)
    ordr = Ordersummery.objects.filter(user=user).order_by('month','-day')

    return render(request, 'client/orders.html',{'orders':ordr})
@login_required(login_url='/')
@authentication(allowed='client')
def orderupdate(request):
    user = User_data.objects.get(user_id = request.user)
    ordr = Ordersummery.objects.filter(user=user,status='undelivered').order_by('month','-day')

    return render(request, 'client/orderUpdate.html',{'orders':ordr})
@login_required(login_url='/')
@authentication(allowed='client')
def placeorder(request):
    user = User_data.objects.get(user_id = request.user)
    hub = user.hub
    if request.method =='POST':
        amnt = request.POST.get('amount')
        quantity = request.POST.get('quantity')
        month_id = request.POST.get('month')
        month = Month.objects.get(id=month_id)
        day_id = request.POST.get('day')
        day = Day.objects.get(id=day_id)
        entry = Ordersummery(user = user,hub = hub, month =month, day = day, amount = amnt, quantity=quantity)
        entry.save()
        return redirect('/user/')

    return render(request, 'client/placeorder.html', {'months':Month.objects.all,'days':Day.objects.all})

@login_required(login_url='/')
@authentication(allowed='client')
def orderupdate2(request,id):
    user = User_data.objects.get(user_id = request.user)
    ordr = Ordersummery.objects.get(id= id,user=user)
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
@authentication(allowed='client')
def trackorder(request):
    return render(request, 'client/trackorder.html')

