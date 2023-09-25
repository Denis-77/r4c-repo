from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from orders.models import Order
from customers.views import send_mail_to_customers


class Robot(models.Model):
    serial = models.CharField(max_length=5, blank=False, null=False)
    model = models.CharField(max_length=2, blank=False, null=False)
    version = models.CharField(max_length=2, blank=False, null=False)
    created = models.DateTimeField(blank=False, null=False)


@receiver(post_save, sender=Robot)
def my_model_post_save(sender, instance, created, **kwargs):
    orders = (
        Order.objects
        .filter(robot_serial=instance.serial)
        .select_related('customer')
    )

    emails = [order.customer.email for order in orders]
    emails = tuple(emails)
    send_mail_to_customers(serial=instance.serial, list_customer=emails)
