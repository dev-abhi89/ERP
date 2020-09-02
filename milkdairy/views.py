from django.shortcuts import render , redirect,HttpResponse
from django.contrib.auth.models import auth, User
from django.contrib import messages
from .models import Members, Hubs, Orders,Day,Month,daysrel
from datetime import date


# Create your views here.

def dashboard(request):
    data = {'hubs':Hubs.objects.all, 'days':Day.objects.all,'months':Month.objects.all}
    if request.user.is_authenticated:
        if request.method == 'POST':
            name = request.POST['name']
            number = request.POST['number']
            amount = request.POST['amount']
            quantity = request.POST['quantity']
            check = request.POST.get('check', 'off') # trigger for membership
            hubs = request.POST['hubs']
            hub = Hubs.objects.get(id=hubs)
            print([name, number, hubs, amount, quantity])#for testing
            entry = Orders(name=name, hub_id= hub, num=number, amount=amount, quantity=quantity )
            entry.save() # for data sumit in user's table
            if check == 'on': #if statement for membership

                ncheck = request.POST.get('ncheck', 'off') # trigger for second month

                monthd = request.POST['months']
                month_id=Month.objects.get(id=monthd)

                usr_id = Orders.objects.latest('id')
                dys = request.POST.getlist('days')



                enter = Members(order_id=usr_id,)
                enter.save()  #data sumit in members's table
                mem = Members.objects.latest('id')



                final = daysrel(user_id=mem, month_id=month_id,)
                final.save()
                ab = daysrel.objects.latest('id')
                for day in dys:
                    daee=Day.objects.get(id = day)
                    ab.day_id.add(daee)

                if ncheck== 'on': #if statement for next month feeding
                    nmonth = request.POST['nxmonths']
                    ndays = request.POST.getlist('ndays')
                    nmonth_id = Month.objects.get(id=nmonth)
                    nfinal = daysrel(user_id= mem, month_id= nmonth_id)

                    nfinal.save()
                    nab = daysrel.objects.latest('id')
                    for day in ndays:
                        ndae= Day.objects.get(id = day)
                        nab.day_id.add(ndae)
                print(ncheck) #final test









        return render(request, 'dashboard.html', data)
    else:
        return redirect('/')


def logout(request):
    auth.logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect('/')


def databse(request):
    if request.user.is_authenticated:
        data = Orders.objects.all()
        hubs = Hubs.objects.all()
        dataa={'data':data, 'hubs':hubs}
        test = Orders.objects.latest('id')
        print(test.id)
        print(test)




        return render(request, 'milk/database.html', dataa)
    else:
        return redirect('/')



def membership(request):
    if request.user.is_authenticated:

        member = Members.objects.all()



        membr={'mam':member,'membership':daysrel.objects.all,'months':Month.objects.all}

        #dataa={'data':order, 'memer':member,'filter':fit,'list':lst}


        return render(request, 'milk/membership.html',membr)
    else:
        return redirect('/')


def hublist(request):
    if request.user.is_authenticated:
        data = {'hubs':Hubs.objects.all}
        return render(request, 'milk/hublist.html',data)
    else:
        return redirect('/')

def analytic(request):
    if request.user.is_authenticated:
        data = Orders.objects.all() #analysis code fol alltime data
        mem = Members.objects.all()
        amt = Orders.objects.values('amount')
        amnt = {at['amount'] for at in amt }
        amont =sum(amnt)
        total = len(data) #here i use len but better understanding you can also use .count method for precise code
        member = len(mem)
        dat = str(date.today())




        today_data = Orders.objects.filter(date=dat)
        ids = today_data.values('id')#getiing ids of orders
        t_id = [i['id'] for i in ids]#making list
        today_mem =[today_data.filter(members__order_id = i) for i in t_id]#grabbing members using user's table date
        tusers_len = len(today_data) #length of todays users (you can also use .count() query instead len
        tmm_len = len(today_mem) # todays members length
        am_data=today_data.values('amount')
        tamnt = {amt['amount'] for amt in am_data}
        sum_tamnt = sum(tamnt) # sum of total amount



        params = {'orders': total,'amount': amont, 'member':member,'torder':tusers_len, 'tmember':tmm_len,'tamount':sum_tamnt}

        return render(request, 'milk/anatytic.html',params)
    else:
        return redirect('/')
def hubdetails(request):
    if request.user.is_authenticated:
        return render(request, 'milk/hubdetails.html')
    else:
        return redirect('/')


def test(request): #this is for testing you have to remove it when everthing is accomplished
    ma = Day.objects.filter(date='3')



    if request.method =='POST':
        name = request.POST.getlist('days')
    else:
        name= 'chutiyapa'



    dat={'days':Day.objects.all,'mem':Members.objects.all, 'ma':ma, 'daysrel':daysrel.objects.all}
  
    data = Orders.objects.values('id')
    da = [dat['id'] for dat in data]
    print(da)


    datE =[Orders.objects.filter(members__order_id=d) for d in da]
    print(datE)




    print(name)
    #ab = Members.objects.get(id=3)
    #day = Day.objects.get(id=2)
    #day.members_id.add(ab)
    #print(day)
    #rst= day.members_id
    #mg=ab.day_set.all()
    #print(mg)
    #print(rst)
    return render(request, 'milk/test.html', dat)



def filterMonth(request, month):
    filter = daysrel.objects.filter(month_id = month)
    months = Month.objects.all()
    day = Day.objects.all()
    params={'members':filter,'days':day, 'months':months,'month':month}

    return render(request,'milk/filterBymonth.html', params)


def filterDay(request, month,day):
     filter = daysrel.objects.filter(month_id = month,day_id=day)
     months = Month.objects.all()
     days = Day.objects.all()
     params = {'months':months, 'day':day, 'days':days,'filter':filter,'month':month}
     return render(request, 'milk/filterByDay.html', params)


def delivery(request):
    return render(request, 'milk/delivery.html')





