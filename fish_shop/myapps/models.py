from django.db import models

# Create your models here.
class register(models.Model):
    username=models.CharField(max_length=20)
    phone=models.IntegerField()
    email=models.EmailField()
    password=models.CharField(max_length=10)


class fish(models.Model):
    fishname=models.CharField(max_length=20)
    fprice=models.IntegerField()
    fstock=models.IntegerField(default=1)
    fimage=models.FileField()
    description=models.CharField(max_length=100)
    category=models.CharField(max_length=20)


class PasswordReset(models.Model):
    user= models.ForeignKey(register,on_delete=models.CASCADE)
    token= models.CharField(max_length=40)


class cart(models.Model):
    user_details=models.ForeignKey(register,on_delete=models.CASCADE)
    product_details=models.ForeignKey(fish,on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1)
    total=models.IntegerField(default=0)
    status=models.CharField(max_length=10,default="in")


class wishlist(models.Model):
    user_details=models.ForeignKey(register,on_delete=models.CASCADE)
    product_details=models.ForeignKey(fish,on_delete=models.CASCADE)



class deliverydetails(models.Model):
    userdetails=models.ForeignKey(register,on_delete=models.CASCADE)
    productdetails=models.ForeignKey(fish,on_delete=models.CASCADE)
    fullname=models.CharField(max_length=20)
    state=models.CharField(max_length=20)
    address=models.CharField(max_length=20)
    pincode=models.IntegerField()
    city=models.CharField(max_length=20)
    quantity = models.IntegerField(default=1)
    total_price= models.IntegerField()
    payment_status = models.CharField(max_length=20, null=True,default='PAID')
    purchase_date = models.DateTimeField(auto_now=True, null=True)
    product_status = models.CharField(max_length=50, null=True, default='Order Placed')
    instruction = models.CharField(max_length=50, null=True, default='Your Order Has Been Successfully Placed')



