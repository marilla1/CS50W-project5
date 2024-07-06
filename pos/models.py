from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver

# Create your models here.

class Suppliers(models.Model):
    address = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    phone = models.IntegerField()
    ruc = models.CharField(max_length=50)
    socialreason = models.CharField(max_length=50) #NombreEmpresaQueMeVende
    status = models.BooleanField(default=1)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Settings(models.Model):
    systemname = models.CharField(max_length=50)
    image = models.ImageField(upload_to='images/yinliao', blank=True, default='default_image')
    address = models.CharField(max_length=50)
    phone = models.IntegerField()
    exchange = models.DecimalField(max_digits=10, decimal_places=2, default=36.70)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Presentation(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    status = models.BooleanField(default=1)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.name}'

class Category(models.Model):
    categoryname = models.CharField(max_length=50)
    status = models.BooleanField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.categoryname}'

class Size(models.Model):
    size = models.CharField(max_length=50)
    status = models.BooleanField(default=1)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.size}'

class Product(models.Model):
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    productname = models.CharField(max_length=50)
    presentation = models.ForeignKey(Presentation, on_delete=models.CASCADE)
    description = models.CharField(max_length=100)
    status = models.BooleanField(default=1)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.productname}'

class ProductDetail(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    code = models.IntegerField(unique=True)

    def __str__(self) -> str:
        return f'{self.code}'

@receiver(pre_save, sender=ProductDetail)
def codeasign(sender, instance, **kwargs):
    if not instance.code:
        last_product_detail = ProductDetail.objects.order_by('-code').first()
         
        if last_product_detail:
            instance.code = last_product_detail.code+1

        else:
            instance.code = 1

class Sale(models.Model):
    customer_name = models.CharField(max_length=50, null=True)
    # sub_total = models.DecimalField(max_digits=10, decimal_places=2)
    # total = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    money_r= models.DecimalField(max_digits=10, decimal_places=2)
    money_change= models.DecimalField(max_digits=10, decimal_places=2)
    code = models.IntegerField(unique=True)
    status = models.BooleanField(default=1)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.customer_name}, {self.Total}, {self.code}'

@receiver(pre_save, sender=Sale)
def codeasign(sender, instance, **kwargs):
    if not instance.code:
        last_sale = Sale.objects.order_by('-code').first()
         
        if last_sale:
            instance.code = last_sale.code+1

        else:
            instance.code = 1

class Sale_detail(models.Model):
    quantity = models.IntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE) 
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.BooleanField(default=1)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.quantity}'

class Sales_returns(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE) 
    quantity = models.IntegerField()
    concept = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.BooleanField(default=1)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.quantity}, {self.concept}'


    



    



