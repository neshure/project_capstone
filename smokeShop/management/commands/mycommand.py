from django.core.management.base import BaseCommand
from smokeShop.models import Product
import json

class Command(BaseCommand):
  help = 'loads scrapped json website data into database'

  def add_arguments(self, parser):
    parser.add_argument('json_file', type=str, help='json file to load')

  def handle(self, *args, **options):
    json_file = options['json_file']
    with open(json_file) as f:
      data = json.load(f)
      category = data['category']
      for product in data['products']:
        price = product['price'].replace('$', '')
        product['price'] = float(price)
        items = Product(title=product['title'], price=product['price'], image=product['image'], alt=product['alt'], category=category)
        items.save()
    self.stdout.write(self.style.SUCCESS('Successfully scrapped data from website'))

  