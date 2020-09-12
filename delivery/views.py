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
        day = dat[-2:]
        month = dat[-5:-3]
        data = Ordersummery.objects.filter(delivery=user,day__date = day, month__m_num =month)
        trnst = Ordersummery.objects.filter(status='undeliverd',day__date = day, month__m_num =month).count()
        dlvrd = Ordersummery.objects.filter(status='deliverd',day__date = day, month__m_num =month).count()
        ofd = Ordersummery.objects.filter(status='out for delivery',day__date = day, month__m_num =month).count()
        if request.method == 'POST':
            ordr = request.POST.get('ordr')
            sts = request.POST.get('status')
            order = Ordersummery.objects.get(id = ordr)
            order.status = sts
            order.save()

        return render(request, 'delivery/delivery.html',{'orders':data ,'transit':trnst, 'out':ofd,'delivered':dlvrd})
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
    user = Deliveryboy.objects.get(users=request.user)
    return render(request, 'delivery/profile.html', {'user':user})
@login_required(login_url='/')
@authentication(allowed='delivery')
def updateprofile(request):
    user = Deliveryboy.objects.get(users = request.user)
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
    return render(request, 'delivery/updateprofile.html',{'user':user})



def orders(request,slug):
    dat = str(date.today())
    dat.split('-')
    day = dat[-2:]
    month = dat[-5:-3]
    if slug == 'in-transit':
        data = Ordersummery.objects.filter(month__m_num =month, day__date=day,status='undelivered')
    elif slug == 'out-for-delivery':
        data = Ordersummery.objects.filter(month__m_num =month, day__date=day,status='out for delivery')
    elif slug == 'delivered':
        data = Ordersummery.objects.filter(month__m_num =month, day__date=day,status='delivered')
    else:
        data = None

    return render(request, 'delivery/orders.html', {'orders':data})
