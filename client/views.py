from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'client/index.html')

def profile(request):
    return render(request, 'client/profile.html')

def update(request):
    return render(request, 'client/update.html')

def order(request):
    return render(request, 'client/orders.html')

def orderupdate(request):
    return render(request, 'client/orderUpdate.html')

def orderupdate2(request):
    return render(request, 'client/orderUpdate2.html')

def trackorder(request):
    return render(request, 'client/trackorder.html')

