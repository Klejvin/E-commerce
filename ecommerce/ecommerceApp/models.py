from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=100, null=True, blank=True)
    category_slug = models.SlugField(primary_key=True, unique=True)

    def __str__(self):
        return f"{self.category_name}"

class Size(models.Model):
    name = models.CharField(max_length=10) # p.sh. "Small", "Large", "42"

    def __str__(self):
        return self.name
    
class Color(models.Model):
    name = models.CharField(max_length=20) # p.sh. "E kuqe", "Black", "White"

    def __str__(self):
        return self.name

class Item(models.Model):
    item_name = models.CharField(max_length=100, null=True, blank=True)
    item_description = models.TextField(null=True, blank=True)
    item_image = models.ImageField(upload_to="item/")
    item_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    discount_percentage = models.IntegerField(default=0)
    item_category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    
    # Masa ekzistuese
    item_sizes = models.ManyToManyField(Size, blank=True)
    
    # SHTESA: Ngjyrat e reja (Many-to-Many)
    item_colors = models.ManyToManyField(Color, blank=True)

    @property
    def starting_price(self):
        """Kthen çmimin më të ulët (me ulje) midis varianteve ose çmimin bazë."""
        variants = self.variants.all()
        if variants.exists():
            # I renditim variantet sipas çmimit të tyre final (me ulje)
            # dhe marrim vlerën e parë (më të lirën)
            sorted_variants = sorted(variants, key=lambda v: v.get_discounted_price)
            return sorted_variants[0].get_discounted_price
        
        # Nëse s'ka variante, kthejmë çmimin bazë të Item
        return self.get_discounted_price
    
    @property
    def get_discounted_price(self):
        if not self.item_price:
            return 0
        if self.discount_percentage and self.discount_percentage > 0:
            discount_amount = (float(self.item_price) * self.discount_percentage) / 100
            return round(float(self.item_price) - discount_amount, 2)
        return float(self.item_price)
    

class ProductVariant(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='variants')
    size_ml = models.CharField(max_length=20) # p.sh. "50ml", "100ml"
    price = models.DecimalField(max_digits=7, decimal_places=2)
    discount_percentage = models.IntegerField(default=0)

    @property
    def get_discounted_price(self):
        if not self.price:
            return 0
        
        if self.discount_percentage and self.discount_percentage > 0:
            discount_amount = (float(self.price) * self.discount_percentage) / 100
            return round(float(self.price) - discount_amount, 2)
        return float(self.price)
    

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    full_name = models.CharField(max_length=255)
    address = models.CharField(max_length=500)
    phone_number = models.CharField(max_length=20)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    items_json = models.TextField() # Ruajmë detajet e shportës si tekst
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Porosia #{self.id} - {self.full_name}"