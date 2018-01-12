from django.db import models
from django.contrib.auth.models import User


class OrdersManager(models.Manager):
    def create_order(self, user_id, department_id, status):
        order = self.create(user_id=user_id, department_id=department_id, status=status)
        return order



class Departments(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=1000)
    picture = models.ImageField(upload_to='static/photo')

    def __unicode__(self):
        dict = {}
        dict['name'] = self.name
        dict['description'] = self.description
        dict['picture_name'] = self.picture.name
        return dict
    class Meta:
        ordering = ['name']
        verbose_name = 'Отдел'
        verbose_name_plural = 'Отделы'


class Orders(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    department_id = models.ForeignKey(Departments, on_delete=models.CASCADE, verbose_name="aaa")
    status = models.BooleanField(default=False)

    objects = OrdersManager()

    def __unicode__(self):
        dict = {}
        dict['user_id'] = self.user_id
        dict['department_id'] = self.department_id
        dict['status'] = self.status
        return dict
    class Meta:
        ordering = ['user_id']
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'




