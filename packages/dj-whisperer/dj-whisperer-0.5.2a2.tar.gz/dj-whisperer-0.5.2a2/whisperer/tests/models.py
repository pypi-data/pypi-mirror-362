import uuid

import django
from django.db import models

if django.VERSION >= (2, 0, 0):
    from django.utils.translation import gettext_lazy as _
else:
    from django.utils.translation import ugettext_lazy as _


class Customer(models.Model):
    email = models.EmailField(_(u'Email'))
    first_name = models.CharField(_("First name"), max_length=255, blank=True)
    last_name = models.CharField(_("Last name"), max_length=255, blank=True)
    phone_number = models.CharField(
        _("Phone number"), null=True, blank=True, max_length=128
    )

    is_active = models.BooleanField(_(u'Is active'), default=True)


class Address(models.Model):
    first_name = models.CharField(_("First name"), max_length=255, blank=True)
    last_name = models.CharField(_("Last name"), max_length=255, blank=True)
    line = models.CharField(verbose_name=_(u'Line of address'), max_length=255)
    is_active = models.BooleanField(default=True)


class Order(models.Model):
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    address = models.ForeignKey(Address, null=True, on_delete=models.SET_NULL)
    number = models.CharField(_("Order number"), max_length=128, db_index=True)
    date_placed = models.DateTimeField(_('Date Placed'), db_index=True)
    amount = models.DecimalField(_("Order amount"), decimal_places=2, max_digits=12)
    discount_amount = models.DecimalField(
        _("Discount"), decimal_places=2, max_digits=12, default=0
    )

    shipping_amount = models.DecimalField(
        _("Shipping charge"), decimal_places=2, max_digits=12, default=0
    )


class Foo(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    name = models.CharField(null=True, max_length=255)
