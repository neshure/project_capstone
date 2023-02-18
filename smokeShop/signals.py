from django.dispatch import receiver
from paypal.standard.ipn.signals import valid_ipn_received
from paypal.standard.ipn.signals import invalid_ipn_received
from .models import Order


#PayPal IPN signals
@receiver(valid_ipn_received)
def valid_ipn_signal(sender, **kwargs):
    ipn = sender
    if ipn.payment_status == 'Completed':
        # payment was successful
        # do something here
        Order.objects.create()

#PayPal IPN signals
@receiver(invalid_ipn_received)
def invalid_ipn_signal(sender, **kwargs):
    ipn = sender
    if ipn.payment_status != 'Completed':
        # payment was not successful
        # do something here
        Order.objects.create()

