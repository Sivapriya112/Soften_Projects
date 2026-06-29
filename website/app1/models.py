from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now
from django.db.models import Avg

# Create your models here.
class user_register(models.Model):
    username = models.CharField(max_length = 100)
    mobile = models.IntegerField()
    email = models.EmailField()
    password = models.CharField(max_length = 100)
    role = models.CharField(max_length = 100)

    def __str__(self):
        return f"{self.username}-{self.role}"


class worker_profile(models.Model):
    SKILL_CHOICE = [('driver', 'Driver'),
        ('plumber', 'Plumber'),
        ('electrician', 'Electrician'),
        ('carpenter', 'Carpenter'),
        ('painter', 'Painter'),
        ('mason', 'Mason'),
        ('cleaner', 'Cleaner'),
        ('security', 'Security Guard'),
        ('delivery', 'Delivery Boy'),
        ('helper', 'Helper / Labour'),
        ('catering', 'Catering Staff'),
    ]

    user = models.OneToOneField(user_register, on_delete=models.CASCADE)
    skill = models.CharField(max_length = 50,choices=SKILL_CHOICE)
    is_online = models.BooleanField(default=False)
    document=models.FileField(null=True,blank=True)
    is_verified=models.BooleanField(default=False)
    is_terminated=models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    def average_rating(self):
        return booking.objects.filter(
            worker=self,
            rating__isnull=False
        ).aggregate(Avg('rating'))['rating__avg'] or 0

    def __str__(self):
        return f"{self.user.username}-{self.skill}"

class booking(models.Model):
    STATUS_CHOICE = [('pending', 'Pending'),
                     ('accepted', 'Accepted'),
                     ('rejected', 'Rejected')]
    user=models.ForeignKey(user_register, on_delete=models.CASCADE)
    worker = models.ForeignKey(worker_profile, on_delete=models.CASCADE)
    requested_date = models.DateField(default=now)
    requested_time = models.TimeField(default=now)
    status=models.CharField(max_length = 20,choices=STATUS_CHOICE,default='pending')
    created_at = models.DateTimeField(auto_now=True)
    work_status = models.CharField(
        max_length=20,
        choices=[
            ('not_started', 'Not Started'),
            ('in_progress', 'In Progress'),
            ('completed', 'Completed'),
        ],
        default='not_started'
    )
    work_start_time = models.DateTimeField(null=True, blank=True)
    work_end_time = models.DateTimeField(null=True, blank=True)
    total_hours = models.FloatField(null=True, blank=True)
    fare = models.FloatField(null=True, blank=True)
    payment_status = models.CharField(
        max_length=20,
        choices=[
            ('unpaid', 'Unpaid'),
            ('paid_cash', 'Paid - Cash'),
            ('paid_online', 'Paid - Online'),
        ],
        default='unpaid'
    )
    is_closed = models.BooleanField(default=False)
    rating = models.IntegerField(null=True, blank=True)
    razorpay_order_id = models.CharField(max_length=200, null=True, blank=True)
    def __str__(self):
        return f"{self.user.username}-{self.worker.user.username}"


class complaint(models.Model):
    user=models.ForeignKey(user_register, on_delete=models.CASCADE)
    worker=models.ForeignKey(worker_profile, on_delete=models.CASCADE)
    message=models.TextField()
    created_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.user.username}-{self.worker.user.username}"
