from django.contrib import admin
from .models import*


class OrdersInline(admin.TabularInline):
    model = Orders
    extra = 0


class DepartmentsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Departments._meta.fields]
    inlines = [OrdersInline]

    class Meta:
        model = Departments

admin.site.register(Departments, DepartmentsAdmin)


class OrdersAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Orders._meta.fields]

    class Meta:
        model = Orders

admin.site.register(Orders, OrdersAdmin)
