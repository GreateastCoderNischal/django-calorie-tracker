from django.shortcuts import render, redirect
from .models import Food, Consume
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout,login
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
# Create your views here.

class CustomLogin(LoginView):
    template_name='myapp/login.html'
    redirect_authenticated_user=True
    
    def get_success_url(self) -> str:
        return reverse_lazy('home')
    def form_invalid(self,form):
        messages.error(self.request,"Incorrect username or password")
        return super().form_invalid(form)
    
def customlogout(request):
    logout(request)
    return redirect('home')

@login_required
def index(request):

    if request.method == "POST":
        food_consumed = request.POST.get('food_consumed','')
        consume = Food.objects.get(name=food_consumed)
        user = request.user
        consume = Consume(user=user, food_consumed=consume)
        consume.save()
        foods = Food.objects.all()

    else:
        foods = Food.objects.all()
    consumed_food = Consume.objects.filter(user=request.user)

    return render(request, 'myapp/index.html', {'foods': foods, 'consumed_food': consumed_food})


def delete_consume(request, id):
    consumed_food = Consume.objects.get(id=id)
    if request.method == 'POST':
        consumed_food.delete()
        return redirect('/')
    return render(request, 'myapp/delete.html')

def register(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        email=request.POST['email']
        user=User.objects.create(username=username,password=password,email=email)
        login(request,user)
        return redirect('home')
    return render(request,'myapp/register.html')
