from django.shortcuts import render
from basic_app.forms import UserForm
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return render(request,'basic_app/index.html')




@login_required 
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def register(request):

    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)

        if user_form.is_valid(): 
            user = user_form.save()
            user.set_password(user.password) 
            user.save()


            registered = True

        else:
            print('user_form.errors') 
    else:
        user_form = UserForm()
    
    return render(request,'basic_app/registration.html',{'user_form':user_form,'registered':registered}) 




def user_login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            
            else:
                return HttpResponse('ACCOUNT NOT ACTIVE')
        else:
            print('Someone tried to login and failed')
            print('Username: {} and passwords {}'.format(username,password))
            return HttpResponse("Invalid login detail Supplied")
    else:

        return render(request,'basic_app/login.html',{})