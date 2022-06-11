import email
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from shortner.models import Users
from shortner.forms import LoginForm, RegisterForm

# Create your views here.


def index(request):
    user = Users.objects.filter(username="admin").first()
    email = user.email if user else "Anonymous"
    print(email)
    print(request.user.is_authenticated)
    if request.user.is_authenticated is False:
        email = "Anonymous"
        print(email)

    return render(request, "base.html", {"welcome_msg": "Hello"})


@csrf_exempt
def get_user(request, user_id):
    print(user_id)
    if request.method == "GET":
        abc = request.GET.get("abc")
        xyz = request.GET.get("xyz")
        user = Users.objects.filter(pk=user_id).first()
        return render(request, "base.html", {"user": user, "params": [abc, xyz]})
    elif request.method == "POST":
        username = request.GET.get("username")
        if username:
            user = Users.objects.filter(pk=user_id).update(username=username)

        return JsonResponse(dict(msg="You just reached with Post Method"))

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        msg = "올바르지 않은 데이터"
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            msg = "회원 가입 완료"
        return render(request, "register.html", {"form": form, "msg": msg})
    else:
        form = RegisterForm()
    return render(request, "register.html", {"form": form})

def login_view(request):
    is_ok = False
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            raw_password = form.cleaned_data.get("password")
            remember_me = form.cleaned_data.get("remember_me")
            msg = "올바른 User ID와 Password를 입력하세요." 
            try:
                user = Users.objects.get(email=email)
            except Users.DoesNotExist:
                pass
            else:
                if user.check_password(raw_password):
                    msg=None
                    login(request, user)
                    is_ok = True
                    request.session["remember_me"] = remember_me
            
    else:
        msg = None
        form = LoginForm()

    return render(request, "login.html", {"form": form, "msg": msg, "is_ok": is_ok})

def logout_view(request):
    logout(request)
    return redirect("login")

@login_required
def list_view(request):
    page = int(request.GET.get("p", 1))
    users = Users.objects.all().order_by("-id")
    paginator = Paginator(users, 10)
    users = paginator.get_page(page)
    
    return render(request, "boards.html", {"users": users})