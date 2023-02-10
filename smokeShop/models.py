from django.conf import settings
from django.db import models



class Product(models.Model):
  title = models.CharField(max_length=255)
  price = models.DecimalField(max_digits=6, decimal_places=2)
  image = models.URLField()
  alt = models.CharField(max_length=255, null=True, blank=True)
 

  def __str__(self):
    return self.title
  
  def get_display_price(self):
    return "{0:2f}".format(self.price/100)



class OrderItem(models.Model):
  item = models.ForeignKey(Product, on_delete=models.CASCADE)

class Order(models.Model):
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  order_item = models.ManyToManyField(OrderItem)
  start_date = models.DateTimeField(auto_now_add=True)
  ordered_date = models.DateTimeField()
  ordered = models.BooleanField(default=False)

  def __str__(self):
    return self.user.username






