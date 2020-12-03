from django.shortcuts import render,redirect,get_object_or_404,HttpResponse
from .forms import RegisterForm, LoginForm
from .models import User
#from django.contrib.auth.models import User
from django.contrib.auth import login, get_user_model, authenticate, logout
from django.views.generic import CreateView, FormView
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.

User = get_user_model()
def register(request):
    form = RegisterForm(request.POST or None, request.FILES or None)
    context = {
            "form" : form
        }
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        email = form.cleaned_data.get("email")
        birthday = form.cleaned_data.get("birthday")
        avatar = form.cleaned_data.get("avatar")

        registeredUser = User(username = username,birthday=birthday,avatar=avatar, email = email)
        registeredUser.set_password(password)
        registeredUser.save()
        login(request, registeredUser)
                
        messages.success(request,"Başarılı Bir Şekilde Kayıt Oldunuz.")
        return redirect("index")
    return render(request,"register.html",context)
        
def loginUser(request):
    form = LoginForm(request.POST or None)

    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = User.objects.filter(username = username)
        if len(user) != 1:
            messages.info(request,"User does not exist.")
            return redirect("index")
        else:
            user = authenticate(username=username, password=password)
            if user is None:
                messages.info(request,"Password doesn't match.")
                return redirect("index")
        messages.success(request,"Giriş Başarılı")
        login(request,user)
        return redirect("index")

def logoutUser(request):
    logout(request)
    messages.success(request,"You are logout succesfully")
    return redirect("index")


@login_required(login_url = "index")
def userPanel(request,username):
    user = get_object_or_404(User, username=username)
    if request.user.is_authenticated and not (request.user.username == username):
        raise Http404
    if request.method == "POST":

        if request.FILES.get('avatar'):
            user.avatar.delete()
            user.avatar = request.FILES.get('avatar')

        if request.POST.get('avatar-clear'):
            user.avatar.delete()

        user.birthday = request.POST.get('birthday')
        user.email = request.POST.get('email')

        if request.POST.get('password') and request.POST.get('confirm'):
            if request.POST.get('password') == request.POST.get('confirm'):
                user.set_password(request.POST.get('password'))
            else:
                messages.warning(request,'Password do not match!', 'danger')
                return render(request,'userPanel.html')
        user.save()
        messages.success(request,'Your profile successfully updated!')
        return redirect('index')
    return render(request, 'userPanel.html',{'username':username})


        
