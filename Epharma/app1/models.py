from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model

class UserRegisterModel(AbstractUser):
    phone = models.CharField(max_length=13)
    usertype = models.CharField(max_length=10,null=True)

class Categories(models.Model):
    category_name=models.CharField(max_length=100,unique=True)

    is_active=models.BooleanField(default=True)
    def __str__(self):
        return self.category_name
class Products(models.Model): 
    product_name=models.CharField(max_length=100,unique=True)
    category=models.ForeignKey(Categories,on_delete=models.CASCADE)
    price=models.PositiveIntegerField()
    selling_price=models.PositiveIntegerField(null=True)
    image=models.ImageField(upload_to="image",null=True) 
    brand=models.CharField(max_length=250,null=True)
    description=models.CharField(max_length=250,null=True)
    def __str__(self):
        return self.product_name
class UploadedFilemodel(models.Model):

    file = models.FileField(upload_to='media') 
    uploaded_at = models.DateTimeField()
    uploaded_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)



class Cart(models.Model):
    user=models.ForeignKey(UserRegisterModel,on_delete=models.CASCADE)
    product=models.ForeignKey(Products,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)

    @property
    def total_cost(self):
        return self.quantity*self.product.selling_price

    
STATE_CHOICES=(

    ('Kerala','Kerala'),
    ('Tamilnadu','Tamilnadu'),
    ('Karnataka','karnataka')

)

class Customer(models.Model):
    
    user=models.ForeignKey(UserRegisterModel,on_delete=models.CASCADE)
    name=models.CharField(max_length=200)
    housename=models.CharField(max_length=200)
    locality=models.CharField(max_length=200)
    city=models.CharField(max_length=50)
    mobile=models.IntegerField(default=0)
    zipcode=models.IntegerField()
    state=models.CharField(choices=STATE_CHOICES,max_length=100)

    def __str__(self):
        return self.name
    
STATUS_CHOICES=(
    ("Accepted",'Accepted'),
    ('Packed','Packed'),
    ('On The way','On The Way'),
    ('Delivered','Delivered'),
    ('Cancel','Cancel'),
    ('Pending','Pending'),
     
)

class Payment(models.Model):

    user=models.ForeignKey(UserRegisterModel,on_delete=models.CASCADE)
    amount=models.FloatField()
    razorpay_order_id=models.CharField(max_length=100,blank=True,null=True)
    razorpay_payment_status=models.CharField(max_length=100,blank=True,null=True)
    razorpay_payment_id=models.CharField(max_length=100,blank=True,null=True)
    paid=models.BooleanField(default=False)

class OrderPlaced(models.Model):
    user=models.ForeignKey(UserRegisterModel,on_delete=models.CASCADE)
    Customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
    product=models.ForeignKey(Products,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    ordered_date=models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=50,choices=STATUS_CHOICES,default='Pending')
    payment=models.ForeignKey(Payment,on_delete=models.CASCADE,default="")
    @property
    def total_cost(self):
        return self.quantity * self.product.selling_price
class Wishlist(models.Model):
    user=models.ForeignKey(UserRegisterModel,on_delete=models.CASCADE)
    product=models.ForeignKey(Products,on_delete=models.CASCADE)

    

