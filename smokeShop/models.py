from django.conf import settings
from django.db import models
from django.db.models import Sum



class Product(models.Model):
  title = models.CharField(max_length=255)
  price = models.DecimalField(max_digits=6, decimal_places=2)
  image = models.URLField()
  alt = models.CharField(max_length=255, null=True, blank=True)
  rating = models.DecimalField(max_digits=2, decimal_places=1, null=True, blank=True)
  
 

  def __str__(self):
    return self.title
  
  def get_display_price(self):
    return "{0:2f}".format(self.price/100)



class OrderItem(models.Model):
  product = models.OneToOneField(Product, on_delete=models.SET_NULL, null=True)
  quantity = models.IntegerField(default=1)
  ordered = models.BooleanField(default=False)
  date_added = models.DateTimeField(auto_now_add=True)
  date_ordered = models.DateTimeField(null=True, blank=True)

  def __str__(self):
    return f"{self.quantity} of {self.product.title}"

class Order(models.Model):
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  order_item = models.ManyToManyField(OrderItem)
  start_date = models.DateTimeField(auto_now_add=True)
  ordered_date = models.DateTimeField(null=True, blank=True)
  ordered = models.BooleanField(default=False)

  def get_cart_items(self):
    return self.order_item.all()

  def get_total_price(self):
    return self.order_item.aggregate(Sum('product__price'))['product__price__sum']

  




