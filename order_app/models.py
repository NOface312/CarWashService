from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth import get_user_model
from accounts.models import User, Service, Company
from django.contrib.auth.models import UserManager


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)


    order_date = models.DateTimeField('Order date', default=timezone.now(), blank=True)

    def __str__(self):
        title = "Order " + str(self.user)
        return title
