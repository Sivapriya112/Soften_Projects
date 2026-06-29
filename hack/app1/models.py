from django.db import models

# Create your models here.
class user_register(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField()
    phone = models.IntegerField()
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    pincode = models.IntegerField(null=True)
    state = models.CharField(max_length=30, null=True)
    city = models.CharField(max_length=30,null=True)
    building_name = models.TextField(null=True)
    road_name = models.CharField(max_length=30,null=True)

class add_product(models.Model):
    name = models.CharField(max_length=30)
    price = models.IntegerField()
    quantity = models.IntegerField()
    image = models.ImageField()

class cart(models.Model):
    user_details = models.ForeignKey(user_register,on_delete=models.CASCADE)
    product_details = models.ForeignKey(add_product,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    total_price = models.IntegerField()

class wishlist(models.Model):
    user_details = models.ForeignKey(user_register,on_delete=models.CASCADE)
    product_details = models.ForeignKey(add_product,on_delete=models.CASCADE)

class orders(models.Model):
    user_details = models.ForeignKey(user_register, on_delete=models.CASCADE)
    product_details = models.ForeignKey(add_product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    amount = models.IntegerField()
    delivery_boy = models.CharField(max_length=30,null=True)
    product_status = models.CharField(max_length=30,default='order placed')
    order_date = models.DateTimeField()

class delivery_boy_register(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField()
    phone = models.IntegerField()
    driving_license_no = models.IntegerField()
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    work_status = models.CharField(max_length=30,default='Free')
    status = models.CharField(max_length=30,default='Pending')

class PasswordReset(models.Model):
    user_details = models.ForeignKey(user_register,on_delete = models.CASCADE)
    token = models.CharField(max_length=255)