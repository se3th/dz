from django.contrib import admin
from my_app.models import OrderModel, ComputerModel, CustomerModel

class CustomerFilter(admin.ModelAdmin):
    pass

class CustomerAdmin(admin.ModelAdmin):
    exclude = ('password', )
    list_filter = ('firstname', 'secondname')
    search_fields = ['id']
    pass

class OrderAdmin(admin.ModelAdmin):
    list_filter = ('status', 'computer__id')


admin.site.register(CustomerModel, CustomerAdmin)
admin.site.register(OrderModel, OrderAdmin)
admin.site.register(ComputerModel)