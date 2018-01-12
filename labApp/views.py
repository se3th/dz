from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import *
from labApp.forms import*

# Create your views here.
class MainPage(TemplateView):
    template_name = 'home.html'


class DepartmentsView(ListView):
    model = Departments
    paginate_by = 4
    template_name = 'departments.html'
    context_object_name = 'departments_list'


class DepartmentView(View):
   def get(self, request, id):
        department = Departments.objects.get(id=id)
        member_list = []
        members = Orders.objects.all()
        for member in members:
            if int(id) == member.department_id_id:
                member_dict = dict()
                user = User.objects.get(id=member.user_id_id)
                member_dict['name'] = user.first_name
                member_dict['lastname'] = user.last_name
                member_list.append(member_dict)
        global err
        err = ''
        if 'mybtn' in request.GET:
            if request.user.is_authenticated():
                current_user = request.user.id
                user_tags = Orders.objects.filter(department_id=id)
                user_list = []
                for user_tag in user_tags:
                    s = user_tag.user_id_id
                    user_list.append(s)
                if current_user not in user_list:
                    new_order = Orders.objects.create_order(department_id=department,user_id=request.user,status=True)
                else:
                    err = "You are already a member of this department"
            else:
                err = "You must be registered to join the department!!"
        return render(request, 'department.html', {"department": department, "member_list": member_list, 'a':err})


class AddDepartmentView(CreateView):
    form_class = AddDepartment
    template_name = 'add_department.html'
    success_url = '/department/'

    def get_success_url(self):
        url = '/department/' + str(self.object.id)
        return url


class Registration(FormView):
    template_name = 'registration.html'
    form_class = RegistrationForm
    success_url = '/success/'

    def post(self, request, *args, **kwargs):
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            return redirect(self.success_url)
        return render(request, self.template_name, {'form': form})


class Autorization(FormView):
    template_name = 'autorization.html'
    form_class = AuthorizationForm
    success_url = '/departments'

    def post(self, request, *args, **kwargs):
        form = AuthorizationForm(data=request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'],password=form.cleaned_data['password'])
            if user is not None and user.is_active:
                login(request,user)
                return redirect(self.success_url)
        return render(request, self.template_name, {'form':form})


@login_required(login_url='/error/')
def login_success(request):
    return HttpResponseRedirect('/departments')


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/error/')


def error_auth(request):
    return render(request, 'home.html')