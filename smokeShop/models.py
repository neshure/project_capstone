from django.conf import settings
from django.db import models
from django.db.models import Sum, Avg



class Product(models.Model):
  title = models.CharField(max_length=255)
  price = models.DecimalField(max_digits=6, decimal_places=2)
  image = models.URLField()
  alt = models.CharField(max_length=255, null=True, blank=True)
  rating = models.DecimalField(max_digits=2, decimal_places=1, null=True, blank=True)
  user_review = models.TextField(null=True, blank=True)
  
 

  def __str__(self):
    return self.title
  
  def get_rating(self):
    rating = Product.objects.filter(id=self.id).aggregate(Avg('rating'))
    return rating




class OrderItem(models.Model):
  product = models.OneToOneField(Product, on_delete=models.SET_NULL, null=True)
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
  order_item = models.ManyToManyField(OrderItem)
  start_date = models.DateTimeField(auto_now_add=True)
  ordered_date = models.DateTimeField(null=True, blank=True)
  ordered = models.BooleanField(default=False)
  

  def get_cart_items(self):
    return self.order_item.all()

  def get_cart_total(self):
    return sum([item.get_price_total() for item in self.order_item.all()])

  




