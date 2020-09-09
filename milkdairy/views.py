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




# Create your views here.

def dashboard(request):
    data = {'orders':Ordersummery.objects.all}
    if request.user.is_authenticated:

        return render(request, 'dashboard.html', data)
    else:
        return redirect('/')


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


def search(request):
    input = request.GET.get('search')
    result = User_data.objects.filter(Q(number__icontains = input) | Q(whatsaap_number__icontains=input)).distinct()
    return render(request, 'milk/search.html', {'result': result} )


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




    return render(request, 'milk/userdetail.html',data )


def databse(request):
    if request.user.is_authenticated:
        data = User_data.objects.all().order_by('name')
        dataa={'data':data, }
        return render(request, 'milk/database.html', dataa)
    else:
        return redirect('/')



def membership(request):
    if request.user.is_authenticated:
        dat = str(date.today())
        dat.split('-')
        day = dat[-1:]
        month = dat[-4:-3]

        member = Ordersummery.objects.filter(month=month, day=day).order_by('month', '-day')



        membr={'mam':member,'months':Month.objects.all, 'days':Day.objects.all}
        return render(request, 'milk/membership.html',membr)
    else:
        return redirect('/')


def hublist(request):
    if request.user.is_authenticated:
        data = {'hubs':Hub_detail.objects.all}
        return render(request, 'milk/hublist.html',data)
    else:
        return redirect('/')

def analytic(request):
    if request.user.is_authenticated:
        # data = Orders.objects.all() #analysis code fol alltime data
        # mem = Members.objects.all()
        # amt = Orders.objects.values('amount')
        # amnt = {at['amount'] for at in amt }
        # amont =sum(amnt)
        # total = len(data) #here i use len but better understanding you can also use .count method for precise code
        # member = len(mem)
        # dat = str(date.today())
        #
        #
        #
        #
        #
        # today_data = Orders.objects.filter(date=dat)
        # ids = today_data.values('id')#getiing ids of orders
        # t_id = [i['id'] for i in ids]#making list
        # today_mem =[today_data.filter(members__order_id = i) for i in t_id]#grabbing members using user's table date
        # tusers_len = len(today_data) #length of todays users (you can also use .count() query instead len
        # tmm_len = len(today_mem) # todays members length
        # am_data=today_data.values('amount')
        # tamnt = {amt['amount'] for amt in am_data}
        # sum_tamnt = sum(tamnt) # sum of total amount
        #
        #
        #
        # params = {'orders': total,'amount': amont, 'member':member,'torder':tusers_len, 'tmember':tmm_len,'tamount':sum_tamnt}

        return render(request, 'milk/anatytic.html')
    else:
        return redirect('/')
def hubdetails(request, id):
    if request.user.is_authenticated:
        hub = Hub_detail.objects.get(id = id)
        dell = Deliveryboy.objects.filter(hub = hub)
        params = {'hub':hub, 'delivery':dell}
        return render(request, 'milk/hubdetails.html',params)
    else:
        return redirect('/')



def filterMonth(request, month):
    filter = Ordersummery.objects.filter(month= month).order_by('month', '-day')
    months = Month.objects.all()
    day = Day.objects.all()
    params={'members':filter,'days':day, 'months':months,'month':month}

    return render(request,'milk/filterBymonth.html', params)


def filterDay(request, month,day):
     filter = Ordersummery.objects.filter(month = month,day=day).order_by('-day')
     months = Month.objects.all()
     days = Day.objects.all()
     params = {'months':months, 'day':day, 'days':days,'members':filter,'month':month}
     return render(request, 'milk/filterByDay.html', params)








