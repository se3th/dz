"""dz URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from labApp.views import*

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$',MainPage.as_view(),name='main_url'),
    url(r'^departments$', DepartmentsView.as_view(), name='departments_url'),
    url(r'department/(?P<id>\d+)$', DepartmentView.as_view(), name='department_url'),
    url(r'^registration/', Registration.as_view(), name='registration'),
    url(r'^authorization/', Autorization.as_view(), name='authorization'),
    url(r'^success/', login_success, name='login'),
    url(r'^error/', error_auth, name='error_auth'),
    url(r'^logout/', logout_view, name='logout'),
    url(r'^add_department/', AddDepartmentView.as_view(), name='add_department_url'),
]
