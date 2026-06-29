from django.db import models

# Create your models here.
class user_details(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    phone_no = models.CharField(max_length=100)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    housename = models.CharField(max_length=255)
    landmark = models.CharField(max_length=255)
    area= models.CharField(max_length=255)
    pincode = models.CharField(max_length=255)
    user_image = models.FileField()
    status = models.CharField(max_length=255,default='active')
    def __str__(self):
        return self.name
    
class services(models.Model):
    service_name = models.CharField(max_length=255)
    service_discription = models.TextField()
    service_amount = models.FloatField()
    service_image = models.FileField(upload_to='services_images/', null=True, blank=True)
    status = models.CharField(max_length=255,default='approved')
    def __str__(self):
        return self.service_name

class BookingOrders(models.Model):
    user = models.ForeignKey(user_details, on_delete=models.CASCADE)
    services = models.CharField(max_length=255)
    car_model = models.CharField(max_length=255)
    car_number = models.CharField(max_length=255)
    date = models.DateField()
    time_slot =models.CharField(max_length= 255)
    payment_amount = models.FloatField(default=0)
    payment_status =models.CharField(max_length=255, default='Pending') 
    status =models.CharField(max_length=255, default='Pending') 
    refund_status =models.CharField(max_length=255,default='0') 
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Booking by {self.user.name} for {self.services} on {self.date} at {self.time_slot}"
    
class PasswordReset(models.Model):
    user_details = models.ForeignKey(user_details,on_delete = models.CASCADE)
    token = models.CharField(max_length=255)
    
#Products models

class Products(models.Model):
    car_name = models.CharField(max_length=255)
    product_name = models.CharField(max_length=255)
    product_image = models.FileField(upload_to='product_images/', null=True, blank=True)
    product_price = models.CharField(max_length=255)
    product_details = models.TextField()
    quantity = models.IntegerField(default=1)
    status = models.CharField(max_length=25,default='approved')
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f" added a {self.product_name} on {self.created_at} "
    
class UserWishlist(models.Model):
    user_details = models.ForeignKey(user_details,on_delete= models.CASCADE)
    product_details = models.ForeignKey(Products,on_delete= models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
class UserCarts(models.Model):
    user_details = models.ForeignKey(user_details,on_delete= models.CASCADE)
    product_details = models.ForeignKey(Products,on_delete= models.CASCADE)
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

class ProductRate(models.Model):
    User = models.ForeignKey(user_details,on_delete = models.CASCADE)
    Product = models.ForeignKey(Products,on_delete= models.CASCADE)
    rate = models.IntegerField(default=1)
    feedback = models.TextField(blank=True)
    def __str__(self):
        return f"Product : {self.Product.product_name} rate by {self.User.username}"

#=================================Delivery Boy ======================================================================



class DeliveryBoy(models.Model):
    name = models.CharField(max_length=100,)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    status = models.CharField(max_length=255,default='not approved')
    work_status = models.CharField(max_length=255,default='free')
    date_joined = models.DateTimeField(auto_now_add=True)
    profile_picture = models.FileField()
    license_number = models.CharField(max_length=255)
    license_image = models.FileField()
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    points = models.IntegerField(default=5)
    def __str__(self):
        return self.name


class ProductsOrders(models.Model):
    user_details = models.ForeignKey(user_details,on_delete= models.CASCADE)
    product_details = models.ForeignKey(Products,on_delete= models.CASCADE)
    quantity = models.IntegerField(default=1)
    payment_amount = models.IntegerField()
    payment_status = models.CharField(max_length=255,default='pending')
    order_status = models.CharField(max_length=255,default='ordered')
    product_code =models.CharField(max_length=4,default='0000')
    delivery_boy = models.ForeignKey(DeliveryBoy,on_delete= models.CASCADE, null=True, blank=True)
    refund_status =models.CharField(max_length=255,default='0') 
    created_at = models.DateTimeField()
    def __str__(self):
        return f"  {self.user_details.username} ordered on {self.created_at} "
    
    
class DPasswordReset(models.Model):
    user_details = models.ForeignKey(DeliveryBoy,on_delete = models.CASCADE)
    token = models.CharField(max_length=255)