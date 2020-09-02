from django.shortcuts import render

# Create your views here.
def delivery(request):
    return render(request, 'delivery/delivery.html')

def orderdetails(request):
    return render(request, 'delivery/orderdetail.html')

def profile(request):
    return render(request, 'delivery/profile.html')

def updateprofile(request):
    return render(request, 'delivery/updateprofile.html')

