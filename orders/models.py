from django.conf import settings
from django.db import models
from decimal import Decimal
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import gettext_lazy as _
from coupons.models import Coupon


# Create your models here.

class Order(models.Model):
    first_name = models.CharField(_('first name'),max_length = 50)
    last_name = models.CharField(_('last name'), max_length = 50)
    email = models.EmailField(_('e-mail'))
    address = models.CharField(_('address'), max_length = 250)
    postal_code = models.CharField(_('postal code'), max_length = 20)
    city = models.CharField(_('city'), max_length = 100)
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now_add = True)
    paid = models.BooleanField(default = False)
    stripe_id = models.CharField(max_length = 250, blank = True)
    coupon = models.ForeignKey(
        Coupon,
        related_name = 'orders',
        null = True,
        blank = True,
        on_delete = models.SET_NULL
    )
    discount = models.IntegerField(
        default = 0,
        validators = [MinValueValidator(0), MaxValueValidator(100)]
    )

    def get_total_weight(self):
        return sum(item.get_weight() for item in self.items.all)

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields = ['-created']),
        ]

    def __str__(self):
        return f'Order {self.id}'
    
    def calculate_shipping_cost(total_weight):
        """
        Calculate shipping cost based on total weight in grams.

        - Upto 1000g: $5
        - 1001g to 5000g: $10
        - 0ver 5000g: $20
        """

        if total_weight <= 1000:
            return Decimal('5.00')
        elif total_weight <=5000:
            return Decimal('10.00')
        else:
            return Decimal('$20.00')

    def get_total_cost(self):
        total_cost = self.get_total_cost_before_discount()
        shipping_cost = self.calculate_shipping_cost(self.get_total_weight())
        return total_cost - self.get_discount() + shipping_cost
    
    def get_stripe_url(self):
        if not self.stripe_id:

            # no payments associated
            return ''
        if '__test__' in settings.STRIPE_SECRET_KEY:
            # stripe path for test payments
            path = '/test/'
        else:

            # stripe path for real payments
            path = '/'
        return f'https://dashboard.strip.com{path}payments/{self.stripe_id}'

    
    def get_total_cost_before_discount(self):
        return sum(item.get_cost() for item in self.items.all())


    def get_discount(self):
        total_cost = self.get_total_cost_before_discount()
        if self.discount:
            return total_cost * (self.discount / Decimal(100))
        return Decimal(0)



class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        related_name = 'items',
        on_delete = models.CASCADE
    )
    product = models.ForeignKey(
        'shop.Product',
        related_name = 'order_items',
        on_delete = models.CASCADE
    )

    price = models.DecimalField(
        max_digits = 10,
        decimal_places = 2
    )

    quantity = models.PositiveIntegerField(default = 1)


    def __str__(self):
        return str(self.id)
    
    def get_cost(self):
        return self.price * self.quantity
    
    def get_weight(self):
        return self.product.weight * self.quantity
    
    