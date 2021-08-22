from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound, Http404

from django.http import HttpResponseRedirect
from django.urls import reverse

from .objects import globals

from .models import *

def index(request):
    user_cookie_value = request.COOKIES.get("user")
    admin_cookie_django = request.COOKIES.get("admin")

    if admin_cookie_django:
        return HttpResponseRedirect(reverse("users"))
    elif user_cookie_value != None:
        return HttpResponseRedirect(reverse("user_profile", args=(user_cookie_value,)))

    data = {"title":"Garant Bot Web", "button_front_name":"Войти", "action":"login/"}

    return render(request, "wgb/index.html", data)

def more_info_user(request, user_id):

    user_data = AuthUser.objects.filter(user_id=user_id).all()[0]
    deals = list(ShopsAndSales.objects.filter(main_user=user_id).all())
    output_apps= list(OutputApplication.objects.filter(user_id=user_id).all())

    if not deals:
        deals = None

    if not output_apps:
        output_apps = None

    all_data = {"title": f"User-{user_data.user_id}","user_data": user_data,
        "deals": deals, "output_apps": output_apps, 
        "button_front_name":"Выйти", "action":"/logout"}

    return render(request, "wgb/more-info-user.html", all_data)

def login(request):
    data = {"message":None}

    if request.POST:
        if "login-button" in request.POST:
            login = request.POST.get("login")
            password = request.POST.get("password")

            if login == "" and password == "":
                data["message"] = "Поля не должны быть пустыми!"
            elif login == "" and password != "":
                data["message"] = "Нужно ввести логин!"
            elif login != "" and password == "":
                data["message"] = "Нужно ввести пароль!"
            else:
                try:
                    check_user = auth(user_data=AuthUser, login=login, password=password)
                    
                    if check_user.is_superuser:
                        completed_auth = HttpResponseRedirect(reverse("users"))
                        completed_auth.set_cookie("admin", True)
                        return completed_auth
                    else:
                        if check_user is not None:
                            data = {"title":"Profile", "user_id":int(check_user.user_id),
                                "button_front_name":"Выйти", "action":"/logout"}

                            completed_auth = HttpResponseRedirect(reverse("user_profile", args=(login,)))
                            completed_auth.set_cookie("user", login)
                            return completed_auth
                        else:
                            data["message"] = "Неверный логин или пароль!"
                except ValueError:
                    data["message"] = "Неверный логин!"

        return render(request, "wgb/login.html", data)

def user_profile(request, user_id):
    cookie_value = request.COOKIES.get("user")

    if cookie_value != None:
        main_data_user = AuthUser.objects.get(user_id=user_id)
        shops = ShopsAndSales.objects.filter(main_user=user_id).all()
        sales = ShopsAndSales.objects.filter(not_main_user=user_id).all()

        percent_together: int = len(shops) + len(sales)
        percent_shops: int = int(len(shops) / percent_together * 100)
        percent_sales: int = int(len(sales) / percent_together * 100)

        data = {"title":"Profile", "button_front_name":"Выйти",
            "action":"/logout", "user_id":user_id, "user":main_data_user,
            "percnet_shops":percent_shops, "percent_sales":percent_sales}

        return render(request, "wgb/profile.html", data)
    else:
        return HttpResponseRedirect(reverse("index"))

def shops(request, user_id):
    shops = ShopsAndSales.objects.filter(main_user=user_id).all()

    if not shops:
        shops = None

    data = {"title":"Покупки", "button_front_name":"Выйти", 
        "action":"/logout", "user_id":user_id, "shops":shops}

    return render(request, "wgb/shops.html", data)

def sales(request, user_id):
    sales = ShopsAndSales.objects.filter(not_main_user=user_id).all()

    if not sales:
        sales = None

    data = {"title":"Продажи", "button_front_name":"Выйти", 
        "action":"/logout", "user_id":user_id, "sales":sales}

    return render(request, "wgb/sales.html", data)


def logout(request):
    data = {"title":"Garant Bot Web", "button_front_name":"Войти", "action":"login/"}

    response = render(request, "wgb/index.html", data)
    response.delete_cookie("user")
    response.delete_cookie("admin")
    return response

## Admin functions

def users(request):
    cookie_value = request.COOKIES.get("admin")

    if cookie_value:
        data = {"title":"Users", "button_front_name":"Выйти", 
             "action":"/logout", "users_data":globals.users_data}

        if request.POST=={}:
            globals.users_data = AuthUser.objects.all()
        else:
            if "sort-users" in request.POST:
                globals.users_data = list(reversed(globals.users_data))

        return render(request, "wgb/users.html", data)
    else:
        raise Http404()

### Another mechanic functions

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def auth(user_data:None, login:int, password:str):
    get_data = user_data.objects.filter(user_id=login).all()

    if len(get_data) <= 0:
        return None
    else:
        get_data = get_data[0]

        if get_data.password != password:
            return None 

    return get_data

def pageNotFound(request, exception):
    return HttpResponseRedirect(reverse("index"))