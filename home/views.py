from django.shortcuts import render
from user.models import User, Resident

# Create your views here.
def home(request):
    obj = User.objects.all()
    res = Resident.objects.all()
    for o in obj:
        print("=============")
        print(dir(o))
        print(o.pk)
        print("=============")

    for o in res:
        print("=============")
        print(dir(o))
        print(o.pk)
        print("=============")
    return render(request, "home/home.html")
