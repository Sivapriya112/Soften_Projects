from django.db import models

# Create your models here.

#login
class user(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    def __str__(self):
        return self.username

#usersignup
class login(models.Model):
    name = models.CharField(max_length=50)
    mob = models.IntegerField()
    email = models.EmailField()
    username = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    def __str__(self):
        return self.username

#adopt
class adopt_table(models.Model):
    username = models.CharField(max_length=50)
    fullname = models.CharField(max_length=50)
    email = models.EmailField()
    mob = models.IntegerField()
    message = models.CharField(max_length=100)
    status = models.CharField(max_length=50)
    def __str__(self):
        return self.username

#serviceapp
class appoinment(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    mob = models.IntegerField()
    pet = models.CharField(max_length=50)
    service = models.CharField(max_length=40)
    date = models.DateField()
    time = models.TimeField(default=True)
    status = models.CharField(max_length=50)
    def __str__(self):
        return self.name

#add product
class addproduct(models.Model):
    productname = models.CharField(max_length=50)
    quantity = models.IntegerField()
    price = models.IntegerField()
    image = models.FileField()

#cart
class cart(models.Model):
    product_details = models.ForeignKey(addproduct,on_delete=models.CASCADE)
    user_details = models.ForeignKey(login,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    total_price = models.IntegerField()

#wishlist
class wishlist(models.Model):
    product_details = models.ForeignKey(addproduct, on_delete=models.CASCADE)
    user_details = models.ForeignKey(login, on_delete=models.CASCADE)

#add adoption
class addadopt(models.Model):
    image = models.FileField()
    breed = models.CharField(max_length=50)
    age = models.IntegerField()
    behaviour = models.CharField(max_length=50)

class myorder(models.Model):
    product_details=models.ForeignKey(addproduct, on_delete=models.CASCADE)
    user_details = models.ForeignKey(login, on_delete=models.CASCADE)
    product_status=models.CharField(max_length=20)
    payment_amount=models.IntegerField()
    order_date=models.DateTimeField()
    quantity=models.IntegerField()

#contact/complaint
class contact_table(models.Model):
    username = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    email = models.EmailField()
    mob = models.IntegerField()
    message = models.CharField(max_length=100)
    def __str__(self):
        return self.username

#reset password
class PasswordReset(models.Model):
    user = models.ForeignKey(login,on_delete=models.CASCADE)
    token = models.CharField(max_length=4)
