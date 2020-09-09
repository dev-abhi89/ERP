from django.shortcuts import render,redirect
from datetime import date
from milkdairy.models import Ordersummery
from .models import Deliveryboy
from django.contrib.auth.decorators import login_required
from milk.decorators import authentication


# Create your views here.
@login_required(login_url='/')
@authentication(allowed='delivery')
def delivery(request):
    if request.user.is_authenticated:
        user = Deliveryboy.objects.get(users= request.user)
        dat = str(date.today())
        dat.split('-')

        day = dat[-1:]
        print(day)
        month = dat[-4:-3]
        data = Ordersummery.objects.filter(delivery=user,day_id = day, month_id =month)
        if request.method == 'POST':
            ordr = request.POST.get('ordr')
            sts = request.POST.get('status')
            order = Ordersummery.objects.get(id = ordr)
            order.status = sts
            order.save()

        return render(request, 'delivery/delivery.html',{'orders':data})
    else:
        return redirect('')
@login_required(login_url='/')
@authentication(allowed='delivery')
def orderdetails(request , id):
    detail = Ordersummery.objects.get(id=id)
    if request.method =='POST':
        s_check = request.POST.get('ucheck')
        print(s_check)
        p_check = request.POST.get('pcheck', 'off')
        print(p_check)
        if s_check == 'on':
            sts = request.POST.get('status')
            detail.status = sts
            detail.save()

        elif p_check == 'on':
            payment = request.POST.get('payment')
            detail.payment =payment
            detail.save()


    return render(request, 'delivery/orderdetail.html',{'order':detail})
@login_required(login_url='/')
@authentication(allowed='delivery')
def profile(request):
    return render(request, 'delivery/profile.html')
@login_required(login_url='/')
@authentication(allowed='delivery')
def updateprofile(request):
    return render(request, 'delivery/updateprofile.html')

