from django.conf import settings
from django.db import models
from decimal import Decimal


from django.db.models import Avg
from django.urls import reverse

import uuid




class Product(models.Model):
  title = models.CharField(max_length=255)
  price = models.DecimalField(max_digits=6, decimal_places=2)
  image = models.URLField()
  alt = models.CharField(max_length=255, null=True, blank=True)
  rating = models.DecimalField(max_digits=2, decimal_places=1, null=True, blank=True)
  user_review = models.TextField(null=True, blank=True)
  category = models.CharField(max_length=255, null=True, blank=True)
  
 

  def __str__(self):
    return self.title

  def get_product_category(self):
    return self.category
  
  def get_rating(self):
    rating = Product.objects.filter(id=self.id).aggregate(Avg('rating'))
    return rating




class OrderItem(models.Model):
  product = models.OneToOneField(Product, on_delete=models.CASCADE)
  quantity = models.IntegerField(default=1)
  ordered = models.BooleanField(default=False)
  date_added = models.DateTimeField(auto_now_add=True)
  date_ordered = models.DateTimeField(null=True, blank=True)


  def __str__(self):
    return f"{self.quantity} of {self.product.title}"

  def get_price_total(self):
    return self.quantity * self.product.price

class Order(models.Model):
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  first_name = models.CharField(max_length=255, null=True, blank=True)
  last_name = models.CharField(max_length=255, null=True, blank=True)
  email = models.EmailField(null=True, blank=True)
  address = models.CharField(max_length=255, null=True, blank=True)
  apartment_address = models.CharField(max_length=255, null=True, blank=True)
  city = models.CharField(max_length=255, null=True, blank=True)
  state = models.CharField(max_length=255, null=True, blank=True)
  zip = models.CharField(max_length=255, null=True, blank=True)
  country = models.CharField(max_length=255, null=True, blank=True)
  billing_address = models.CharField(max_length=255, null=True, blank=True)
  billing_apartment_address = models.CharField(max_length=255, null=True, blank=True)
  billing_city = models.CharField(max_length=255, null=True, blank=True)
  billing_state = models.CharField(max_length=255, null=True, blank=True)
  billing_zip = models.CharField(max_length=255, null=True, blank=True)
  billing_country = models.CharField(max_length=255, null=True, blank=True)
  order_item = models.ManyToManyField(OrderItem)
  start_date = models.DateTimeField(auto_now_add=True)
  ordered_date = models.DateTimeField(auto_now=True)
  ordered = models.BooleanField(default=False)

  

  def get_cart_items(self):
    return self.order_item.all()

  def get_cart_total(self):
    return sum([item.get_price_total() for item in self.order_item.all()])
  
  
  


  


#Payment Model
class Payment(models.Model):
  PAYMENT_CHOICES = (
    ('S', 'Stripe'),
    ('P', 'PayPal')
  )
  STATUS_CHOICES = (
    ('P', 'Pending'),
    ('D', 'Delivered'),
    ('C', 'Cancelled')
  )
  amount = models.DecimalField(max_digits=6, decimal_places=2, default=Decimal('0.00'))
  payment_method = models.CharField(max_length=1, choices=PAYMENT_CHOICES, default='P')
  transaction_id = models.UUIDField(default=uuid.uuid4, editable=False)
  status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P')
  order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='payments', null=True, blank=True)
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f'Payment #{self.id} ({self.payment_method}, {self.amount}) for order #{self.order.id}'

