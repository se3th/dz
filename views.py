from django.contrib.auth import authenticate, login as login_user, logout
from django.shortcuts import render, redirect
import os
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
import datetime
from django.views import View
from my_app.models import ComputerModel, CustomerModel, OrderModel
from lab5.settings import BASE_DIR, LOGIN_URL, STATICFILES_DIRS
from .forms import RegisterForm, AuthorizeForm, ComputerForm, OrderForm
from hashlib import md5, sha256
from django.contrib.auth.hashers import *
from django.contrib.auth.models import User
import json, math
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



def basepage(request):
    return render(request, "my_app/base.html")


def basextend(request):
    colors = {
        'colors': {"black": "#000000", "white": "#FFFFFF", "red1": "#FF0000", "green": "#00FF00", "blue": "#0000FF"}}
    return render(request, "my_app/basextend.html", colors)


def testpage(request):
    pages = [
        {'title': "Первая страница", "id": 1},
        {'title': "Вторая страница", "id": 2},
        {'title': "Третья страница", "id": 3}
    ]
    server_times = {'date': datetime.datetime.now()}
    dicts = {"pages": pages, "server_times": server_times}
    return render(request, "my_app/index.html", dicts)


def orderview(request):
    return render('my_app/ordermodal.html')


class PageView(View):
    def post(self, request, id):
        # Adding New Computer ajax
        names_dict = {}
        errors = []
        newobjectform = OrderForm(request.POST, request.FILES)
        if request.method == "POST" and newobjectform.is_valid() and request.is_ajax():
            allowed_files = ['png', 'svg', 'jpeg', 'jpg', 'gif']
            data = newobjectform.cleaned_data
            names_list = ["date_completed"]
            names_dict = {x: request.POST.get(x, "") for x in names_list}

            date_completed = data["date_completed"]
            if not date_completed:
                errors.append('Введите необходимую дату исполнения заказа')

            msg = ""
            if not errors:
                customer_data = CustomerModel.objects.get(login__exact=request.user.username)
                computer_data = ComputerModel.objects.get(id=id)

                OrderModel.objects.create(customer=customer_data, computer=computer_data, date_completed=date_completed,
                                          date_received=datetime.date.today(), status=False)

                msg = "Заказ успешно добавлен!" + " " + "Логин: " + str(
                    customer_data.login) + " " + "Компьютер: " + str(computer_data.name)
            json_response = json.dumps({'errors': errors, 'msg': msg})
            return HttpResponse(json_response, content_type="application/json")
        json_response = json.dumps({'errors': errors, 'msg': "Something went wrong, try again"})
        return HttpResponse(json_response, content_type="application/json")

    def get(self, request, id):
        plist = os.listdir(os.path.join(BASE_DIR, "static"))
        pics = {el.rsplit('.', 1)[0]: el for el in plist}
        computer = ComputerModel.objects.get(id=int(id))
        customers = []
        customers = CustomerModel.objects.values('login').filter(ordermodel__computer_id=int(id)).distinct()
        newobjectform = OrderForm(request.POST or None)
        return render(request, 'my_app/page.html',
                      {'computer': computer, 'pics': pics, 'customers': customers, 'newobjectform': newobjectform})


class IncludePage(View):
    def get(self, request):
        return render(request, 'my_app/inclpage.html')

"""
def authorization(request):
    names_dict = {}
    errors = []

    if request.method == "POST":
        names_list = ["username", "password"]
        names_dict = {x: request.POST.get(x, "") for x in names_list}
        username = request.POST.get("username")
        if not username:
            errors.append('Введите логин')
        password = request.POST.get('password')
        if not password:
            errors.append("Введите пароль")
        if not errors:
            return HttpResponseRedirect("/computers/")
    print(list(errors))
    return render(request, 'my_app/authorization.html', {"errors": errors, 'names_dict': names_dict})
"""


# Форма средствами Django
def RegisterDjango(request):
    names_dict = {}
    errors = []
    form = RegisterForm(request.POST or None)
    # TODO заменить на методы класса
    if request.method == "POST" and form.is_valid():
        data = form.cleaned_data
        names_list = ["firstname", "password", "email", "secondname", "login", "password2"]
        names_dict = {x: request.POST.get(x, "") for x in names_list}

        login = data["login"]

        if not login:
            errors.append('Введите логин')
        elif len(login) < 5:
            errors.append("Логин должен содержать не менее 5 симоволов")

        password = data['password']
        if not password:
            errors.append("Введите пароль")
        elif len(password) < 8:
            errors.append("Длина пароля должна быть не менее 8 символов")
        elif password != data["password2"]:
            errors.append("Пароли не совпадают")

        email = data['email']
        if not email:
            errors.append("Введите e-mail")

        firstname = data['firstname']
        if not firstname:
            errors.append("Введите Имя")

        secondname = data['secondname']
        if not secondname:
            errors.append("Введите Фамилию")

        if not errors:
            # updating data for registration
            new_form = form.save(commit=False)
            new_form.login = data.get('login')
            new_form.firstname = data.get('firstname')
            new_form.secondname = data.get('secondname')
            new_form.password = data.get('password')
            new_form.email = data.get('email')

            user = User.objects.create_user(username= new_form.login, password=new_form.password, email = new_form.email)
            print(user.password)
            new_form.password = user.password
            print(new_form.password)
            new_form.save()
            form.save_m2m()
            return HttpResponseRedirect("/authorize/")
    return render(request, 'my_app/register.html', {"errors": errors, 'names_dict': names_dict, "form": form})


def AuthorizeDjango(request):
    names_dict = {}
    errors = []
    form = AuthorizeForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        data = form.cleaned_data
        names_list = ["login", "password"]
        names_dict = {x: request.POST.get(x, "") for x in names_list}

        login = data["login"]
        if not login:
            errors.append('Введите логин')
        password = data['password']

        if not password:
            errors.append("Введите пароль")

        if not errors:
            try:
                userdata = CustomerModel.objects.get(login=data["login"])
                if not check_password(data.get('password'), userdata.password):
                    errors.append("Неправильное имя пользователя или пароль")

            except CustomerModel.DoesNotExist:
                errors.append("Неправильное имя пользователя")

            if not errors:
                user = authenticate(username=login, password=data.get('password'))
                if user is not None:
                    if request.user.is_authenticated():
                        pass
                    login_user(request, user)
                    return HttpResponseRedirect("/computers/")
    print(list(errors))
    return render(request, 'my_app/authorize.html', {"errors": errors, 'names_dict': names_dict, "form": form})


class ComputersClass(View):
    def post(self, request):
        if request.content_type == "multipart/form-data":
            # Adding New Computer ajax
            filename = ""
            names_dict = {}
            errors = []
            newobjectform = ComputerForm(request.POST, request.FILES)
            if request.method == "POST" and newobjectform.is_valid():

                image = False
                data = newobjectform.cleaned_data
                names_list = ["name", "description"]
                names_dict = {x: request.POST.get(x, "") for x in names_list}

                name = data["name"]
                if not name:
                    errors.append('Введите название')
                if (len(name) < 5):
                    errors.append("Название должно содержать не менее 5 символов")
                description = data['description']
                if not description:
                    errors.append("Введите Описание")
                msg = ""
                if not errors:
                    print(STATICFILES_DIRS[0] + "\\" + data.get('name').lower() + '.txt')

                    new_form = newobjectform.save(commit=False)
                    filepath = str(STATICFILES_DIRS[0] + "\\" + data.get('name').lower() + '.txt')
                    new_form.name = data.get('name')
                    new_form.description = data.get('description')
                    new_form.save()
                    newobjectform.save_m2m()
                    print(data.get('file'))
                    if request.FILES['file']:
                        with open(filepath, 'wb+') as destination:
                            for chunk in request.FILES['file'].chunks():
                                destination.write(chunk)
                    msg = "Объект успешно добавлен!"
                    filename = data.get('name').lower()
                json_response = json.dumps({'errors': errors, 'msg': msg, 'filename': filename})
                return HttpResponse(json_response, content_type="application/json")

            json_response = json.dumps({'errors': errors, 'msg': "Something went wrong, try again"})
            return HttpResponse(json_response, content_type="application/json")

    def get(self, request):
        newobjectform = ComputerForm(request.POST or None)
        if not request.user.is_authenticated:
            return redirect('%s?next=%s' % (LOGIN_URL, request.path))
        computers = ComputerModel.objects.all().count()
        page_quantity = math.ceil(computers / 7)
        return render(request, 'my_app/computers.html',
                      {'user': request.user.username,
                       "newobjectform": newobjectform, "page_quantity": page_quantity})


# Infinite scrolling, use computers.get before
class InfiniteScroll(View):
    def get(self, request):
        action = request.GET.get('action', "")
        if (action == 'infinite_scroll'):
            plist = os.listdir(os.path.join(BASE_DIR, "static"))
            computers = ComputerModel.objects.all()
            page = request.GET.get('page_number', 1)
            paginator = Paginator(computers, 7)
            try:
                numbers = paginator.page(page)
            except PageNotAnInteger:
                numbers = paginator.page(1)
            except EmptyPage:
                numbers = paginator.page(paginator.num_pages)
            pics = {el.rsplit('.', 1)[0]: el for el in plist}
            return render(request, 'my_app/inf_page_element.html',
                          {'numbers': numbers, "pics": pics, 'user': request.user.username})


def LogoutClass(request):
    var = request.user.is_authenticated()
    if request.user.is_authenticated():
        logout(request)
    return redirect('AuthorizeDjango')


"""
def RegisterClass(request):
    names_dict = {}
    errors = []

    if request.method == "POST":
        names_list = ["username", "password", "password2", "email", "firstname", "secondname"]
        names_dict = {x: request.POST.get(x, "") for x in names_list}
        for k, v in names_dict.items():
            print("{}:{}".format(k, v))
        username = request.POST.get("username")
        if not username:
            errors.append('Введите логин')
        elif len(username) < 5:
            errors.append("Логин должен содержать не менее 5 симоволов")
        password = request.POST.get('password')
        if not password:
            errors.append("Введите пароль")
        elif len(password) < 8:
            errors.append("Длина пароля должна быть не менее 8 символов")
        password_repeat = request.POST.get("password2")
        if password != password_repeat:
            errors.append("Пароли должны совпадать")
        if not errors:
            return HttpResponseRedirect("/computers/")
    return render(request, 'my_app/registration.html', {"errors": errors, 'names_dict': names_dict, })
"""
