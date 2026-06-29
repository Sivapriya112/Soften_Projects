
from django.db import models
class Register_user(models.Model):
    Username=models.CharField(max_length=20,unique=True)
    Email=models.EmailField(unique=True)
    Phoneno=models.CharField(max_length=10)
    Password=models.CharField(max_length=12)

    def __str__(self):
        return self.Username
class Register_manager(models.Model):
    Username=models.CharField(max_length=20,unique=True)
    Email=models.EmailField()
    Phoneno=models.CharField(max_length=10)
    Experience=models.IntegerField()
    Password=models.CharField(max_length=12)
    Status=models.CharField(max_length=12,default='pending')
    def __str__(self):
        return self.Username
class User_contact(models.Model):
    Username = models.CharField(max_length=20)
    Email = models.EmailField()
    Phoneno = models.CharField(max_length=10)
    issue= models.CharField(max_length=100)
    eventname= models.CharField(max_length=100)
    query= models.CharField(max_length=100)
    def __str__(self):
        return self.Username

class Subscribe(models.Model):
    Email=models.EmailField()
    def __str__(self):
        return self.Email

class Images(models.Model):
    image = models.ImageField()

class Events(models.Model):
    Event_name= models.CharField(max_length=20)
    Location= models.CharField(max_length=40)
    Date= models.CharField(max_length=10)
    Time= models.CharField(max_length=10)
    Gold_Ticket_price= models.CharField(max_length=10)
    Silver_Ticket_price = models.CharField(max_length=10)
    Bronze_Ticket_price = models.CharField(max_length=10)
    Gold_Available_tickets= models.IntegerField()
    Silver_Available_tickets = models.IntegerField()
    Bronze_Available_tickets = models.IntegerField()
    Event_image=models.FileField()
    Status = models.CharField(max_length=12, default='pending')
    Discription=models.CharField(max_length=100)
    Sub_images = models.ManyToManyField(Images,null=True)
    Video = models.FileField(null=True)
    def __str__(self):
        return self.Event_name


class PasswordReset(models.Model):
    user= models.ForeignKey(Register_user,on_delete=models.CASCADE)
    token= models.CharField(max_length=40)

class Booking(models.Model):
    user_details=models.ForeignKey(Register_user,on_delete=models.CASCADE)
    ticket_details=models.ForeignKey(Events,on_delete=models.CASCADE)
    no_of_tickets=models.IntegerField(default=1)
    total_amount=models.IntegerField(default=0)
    payment_status = models.CharField(max_length=20, null=True, default='PAID')
    booked_date = models.DateTimeField(auto_now=True, null=True)
    ticket_status = models.CharField(max_length=50, null=True, default='BOOKED')









