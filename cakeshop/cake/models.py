from django.db import models

# Create your models here.

class register(models.Model):
    username = models.CharField(max_length=20)
    phone = models.IntegerField()
    email = models.EmailField()
    password = models.CharField(max_length=10)
    address = models.CharField(max_length=200, default='NIL')
    address_city = models.CharField(max_length=20)
    address_district = models.CharField(max_length=20)
    address_state = models.CharField(max_length=20)
    address_pincode = models.IntegerField(default=0)

    def __str__ (self):
        return self.username


class Add_Product(models.Model):
    ProductName=models.CharField(max_length=30)
    Price=models.IntegerField()
    Quantity=models.CharField(max_length=10)
    Models=models.CharField(max_length=20)
    Category =models.CharField(max_length=10)
    image=models.FileField()
    def __str__ (self):
        return self.ProductName

class cart(models.Model):
    product_details = models.ForeignKey(Add_Product, on_delete=models.CASCADE)
    user_details=models.ForeignKey(register,on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1)
    total_price=models.IntegerField(default=0)


class whishlist(models.Model):
    product_details = models.ForeignKey(Add_Product, on_delete=models.CASCADE)
    user_details=models.ForeignKey(register,on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1)


class PasswordReset(models.Model):
    user= models.ForeignKey(register,on_delete=models.CASCADE)
    token=models.CharField(max_length=4)


class dboy(models.Model):
    name = models.CharField(max_length=20)
    email = models.EmailField()
    phno = models.IntegerField()
    d_license = models.FileField()
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=10)
    c_password = models.CharField(max_length=10)
    status = models.CharField(max_length=20, default='pending')
    work_status = models.CharField(max_length=20, default='free')



class order_details(models.Model):
    user_details=models.ForeignKey(register, on_delete=models.CASCADE)
    product_details=models.CharField(max_length=20)
    qunatity=models.IntegerField(default=1)
    total_price=models.IntegerField()
    payment_status=models.CharField(max_length=20,default='NOT PAID')
    delivery_status=models.CharField(max_length=20,default='pending')
    dboy_name=models.CharField(max_length=20,default='abc')
    address = models.CharField(max_length=200, default='NIL')
    address_city = models.CharField(max_length=20)
    address_district = models.CharField(max_length=20)
    address_state = models.CharField(max_length=20)
    address_pincode = models.IntegerField(default=0)

