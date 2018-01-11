from django.db import models


class ComputerModel(models.Model):
    class Meta:
        db_table = 'my_app_computer'
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=255)
    picpath = models.CharField(max_length=255, blank=True, default="")

    def __str__(self):
        return " id: {}, name:{}, description:{}".format(self.id, self.name, self.description, self.picpath)


class CustomerModel(models.Model):
    class Meta:
        db_table = 'my_app_customer'

    login = models.CharField(max_length=64, default='')
    secondname = models.CharField(max_length=64, default='')
    firstname = models.CharField(max_length=64, default='')
    email = models.CharField(max_length=64)
    password = models.CharField(max_length=300)
    computers = models.ManyToManyField(ComputerModel, through='OrderModel')

    def __str__(self):
        return "id : {}, login:{}, secondname:{}, firstname:{}, email:{}".format(self.id, self.login,
                                                                                              self.secondname,
                                                                                              self.firstname,
                                                                                              self.email,
                                                                                              )


class OrderModel(models.Model):
    class Meta:
        db_table = 'my_app_order'

    customer = models.ForeignKey(CustomerModel, on_delete=models.CASCADE)
    computer = models.ForeignKey(ComputerModel, on_delete=models.CASCADE)
    date_received = models.DateField()
    date_completed = models.DateField()
    status = models.BooleanField(default=False)

    def __str__(self):
        return " customer:{}, computer:{}, date_received:{}, date_completed:{}, status:{}".format(
            self.customer,
            self.computer,
            self.date_received,
            self.date_completed,
            self.status)
