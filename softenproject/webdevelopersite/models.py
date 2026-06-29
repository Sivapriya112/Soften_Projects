from enum import unique

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.fields import IntegerField


# Create your models here.
class userregister(models.Model):
    name=models.CharField(max_length=100)
    phone=models.CharField(max_length=100)
    email=models.EmailField()
    username=models.CharField(max_length=100)
    password=models.CharField(max_length=100)

class developerregister(models.Model):
    name=models.CharField(max_length=100)
    phone=models.CharField(max_length=100)
    email = models.EmailField()
    skills=models.CharField(max_length=100)
    experience=models.CharField(max_length=100)
    image=models.ImageField(null=True)
    bio=models.CharField(max_length=100,null=True)
    username=models.CharField(max_length=100)
    password=models.CharField(max_length=100)
    status=models.CharField(max_length=100,default='pending',null=True)

from django.db import models


# CATEGORY TABLE

class Category(models.Model):

    category_name = models.CharField(max_length=100,unique=True)

    def __str__(self):
        return self.category_name


# TECHNOLOGY TABLE

class Technology(models.Model):

    technology_name = models.CharField(max_length=100,unique=True)

    def __str__(self):
        return self.technology_name


# PROJECT TABLE

class createproject(models.Model):
    user = models.ForeignKey(userregister, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    budget = models.IntegerField()
    deadline = models.DateField()
    status = models.CharField(max_length=50, default='pending')
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE
    )

    technologies = models.ManyToManyField(
        Technology
    )

    progress=models.IntegerField(default=0)
    created_at = models.DateTimeField(
        auto_now_add=True
    )


class userreview(models.Model):
    user = models.ForeignKey(userregister, on_delete=models.CASCADE)
    developer = models.ForeignKey(developerregister, on_delete=models.CASCADE, )
    project = models.ForeignKey(createproject, on_delete=models.CASCADE)
    review = models.TextField()
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

class developerportfolio(models.Model):
    developer = models.ForeignKey(developerregister, on_delete=models.CASCADE)

    project_title = models.CharField(max_length=200)
    project_description = models.TextField()
    project_type = models.CharField(max_length=50, null=True)
    project_technology = models.CharField(max_length=50, null=True)
    project_duration = models.IntegerField(null=True)
    project_demo = models.URLField(null=True)

    def __str__(self):
        return self.project_title


class PortfolioImage(models.Model):
    portfolio = models.ForeignKey(
        developerportfolio,
        on_delete=models.CASCADE,
        related_name='images'
    )

    image = models.ImageField(upload_to='portfolio/')

class developerproposal(models.Model):
    developer= models.ForeignKey(developerregister, on_delete=models.CASCADE,)
    project=models.ForeignKey(createproject,on_delete=models.CASCADE)
    project_proposal=models.CharField(max_length=200)
    project_budget=models.IntegerField(null=True)
    progress=models.IntegerField(default=0)
    project_status=models.CharField(max_length=50,null=True,default='pending')
    advance_pay=IntegerField(null=True)
    advance_status = models.CharField(max_length=50, default='pending')
    final_payment_status = models.CharField(max_length=50, default='pending')
    admin_commission = models.IntegerField(default=0)


class worksubmission(models.Model):
    project = models.ForeignKey(createproject,on_delete=models.CASCADE)
    developer = models.ForeignKey(developerregister,on_delete=models.CASCADE)
    file = models.FileField(null=True)
    description = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    upload_status = models.CharField(max_length=50, default='pending')
    payment_status = models.CharField(max_length=50, default='pending')

# class Message(models.Model):
#     project = models.ForeignKey(createproject, on_delete=models.CASCADE)
#     user = models.ForeignKey(userregister, on_delete=models.CASCADE, null=True, blank=True)
#     developer = models.ForeignKey(developerregister, on_delete=models.CASCADE, null=True, blank=True)
#     message = models.TextField()
#     timestamp = models.DateTimeField(auto_now_add=True)


# class Message(models.Model):
#     project = models.ForeignKey(createproject, on_delete=models.CASCADE)
#
#     sender_user = models.ForeignKey(
#         userregister, on_delete=models.CASCADE, null=True, blank=True
#     )
#     sender_developer = models.ForeignKey(
#         developerregister, on_delete=models.CASCADE, null=True, blank=True
#     )
#
#     message = models.TextField()
#     timestamp = models.DateTimeField(auto_now_add=True)
#
#     def sender_name(self):
#         if self.sender_user:
#             return self.sender_user.username
#         elif self.sender_developer:
#             return self.sender_developer.username
#         return "Unknown"
#
#     def is_user(self):
#         return self.sender_user is not None

class payment(models.Model):
    project = models.ForeignKey(createproject, on_delete=models.CASCADE)
    user = models.ForeignKey(userregister, on_delete=models.CASCADE)
    amount = models.IntegerField()
    payment_type = models.CharField(max_length=50)  # advance / final
    payment_status = models.CharField(max_length=50, default='pending')  # pending, paid
    razorpay_order_id = models.CharField(max_length=200, null=True, blank=True)
    razorpay_payment_id = models.CharField(max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)



import uuid
from django.db import models


class PasswordReset(models.Model):

    email = models.EmailField()
    token = models.CharField(max_length=200, unique=True)
    user_type = models.CharField(max_length=50)

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):

        if not self.token:
            self.token = str(uuid.uuid4())

        super().save(*args, **kwargs)

class ChatRoom(models.Model):
    student = models.ForeignKey(userregister, on_delete=models.CASCADE)
    developer = models.ForeignKey(developerregister, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Message(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    sender = models.CharField(max_length=20)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

class AdminCommission(models.Model):
    project = models.ForeignKey(createproject,on_delete=models.CASCADE)
    developer = models.ForeignKey(developerregister,on_delete=models.CASCADE)
    total_amount = models.IntegerField()
    admin_amount = models.IntegerField()
    developer_amount = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)