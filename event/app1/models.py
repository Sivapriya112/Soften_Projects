from django.db import models
from datetime import date
from datetime import timedelta
from decimal import Decimal
from django.utils import timezone


class UserRegister(models.Model):
    CATEGORY_CHOICES = [
        ('user', 'User'),
        ('tailor', 'Tailor'),
        ('catering', 'Catering'),
        ('entertainer', 'Entertainer')
    ]
    username = models.CharField(max_length=150, null=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    password = models.CharField(max_length=128)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='user')
    is_confirmed = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.category == 'user':
            self.is_confirmed = True  # Automatically confirm 'user' category
        super(UserRegister, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} ({self.category})"


class Events(models.Model):
    img = models.ImageField(upload_to="pic")
    name = models.CharField(max_length=50)
    desc = models.CharField(max_length=300)

    def __str__(self):
        return self.name


class Gallery(models.Model):
    image1 = models.ImageField(default='parti.jpg', upload_to='pic')
    image2 = models.ImageField(default='parti.jpg', upload_to='pic')
    image3 = models.ImageField(default='parti.jpg', upload_to='pic')
    image4 = models.ImageField(default='parti.jpg', upload_to='pic')
    image5 = models.ImageField(default='parti.jpg', upload_to='pic')
    image6 = models.ImageField(default='parti.jpg', upload_to='pic')


class Video(models.Model):
    title = models.CharField(max_length=255, help_text="Title of the video")
    description = models.TextField(blank=True, null=True, help_text="Brief description of the video")
    video_file = models.FileField(upload_to='pic', help_text="Upload the video file")
    uploaded_at = models.DateTimeField(auto_now_add=True, help_text="Timestamp when the video was uploaded")

    def __str__(self):
        return self.title


class Shorts(models.Model):
    title = models.CharField(max_length=255, help_text="Title of the video")
    description = models.TextField(blank=True, null=True, help_text="Brief description of the video")
    video_file = models.FileField(upload_to='pic', help_text="Upload the video file")
    uploaded_at = models.DateTimeField(auto_now_add=True, help_text="Timestamp when the video was uploaded")

    def __str__(self):
        return self.title


STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('confirmed', 'Confirmed'),
    ('canceled', 'Canceled'),
    ('completed', 'Completed'),
    ('refunded', 'Refunded'),
    ('paid', 'Paid'),
]


class Booking(models.Model):
    PENDING = 'pending'
    CONFIRMED = 'confirmed'
    CANCELLED = 'cancelled'
    COMPLETED = 'completed'
    REFUNDED = 'refunded'
    PAID = 'paid'

    user_details = models.ForeignKey('UserRegister', on_delete=models.CASCADE)
    phone = models.CharField(max_length=10)  # Allows inclusion of country codes
    event = models.ForeignKey('Events', on_delete=models.CASCADE, related_name='bookings')
    address = models.CharField(max_length=200)
    booking_date = models.DateField()
    booked_on = models.DateField(auto_now=True)
    advance_payment = models.DecimalField(max_digits=10, decimal_places=2, default=5000.00)
    payment_id = models.CharField(max_length=255, null=True, blank=True)
    total_payment = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    refund_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    refund_processed = models.BooleanField(default=False)
    balance_payment = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_payment_updated = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)

    class Meta:
        ordering = ['-booked_on']
        verbose_name = 'Booking'
        verbose_name_plural = 'Bookings'

    def confirm_booking(self):
        """Confirm the booking."""
        self.status = 'confirmed'
        self.save()

    def cancel_booking(self):
        """Cancel the booking."""
        self.status = 'canceled'
        self.save()

    def complete_booking(self):
        """Mark the booking as completed."""
        self.status = 'completed'
        self.save()

    def refund_booking(self):
        """Mark the booking as completed."""
        self.status = 'refunded'
        self.save()

    def calculate_refund(self):
        if self.status != self.CANCELLED:
            return Decimal('0.00')

        # Refund logic based on cancellation time
        days_before_event = (self.booking_date - timezone.now().date()).days

        # Refund based on the advance payment made by the user
        if days_before_event >= 7:  # Full refund if canceled 7 or more days before the event
            return self.advance_payment  # Return the full advance payment
        elif 3 <= days_before_event < 7:  # 50% refund if canceled 3-7 days before the event
            return self.advance_payment * Decimal(0.5)
        else:  # No refund if canceled within 3 days of the event
            return Decimal('0.00')

    def save(self, *args, **kwargs):
        # Automatically calculate refund if booking is cancelled
        if self.status == self.CANCELLED:
            self.refund_amount = self.calculate_refund()

        # Set balance_payment to 0 if status is PAID or REFUNDED
        if self.status in {self.PAID, self.REFUNDED}:
            self.balance_payment = Decimal('0.00')

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user_details.username} - {self.event} ({self.status})"


class PasswordReset(models.Model):
    user = models.ForeignKey(UserRegister, on_delete=models.CASCADE)
    token = models.CharField(max_length=64, unique=True)


class Stories(models.Model):
    image = models.ImageField(default='dj.jpg', upload_to='pic')
    name = models.CharField(max_length=50)
    desc = models.CharField(max_length=500, default='nothing')


class Resort(models.Model):
    image = models.ImageField(default='resort1.jpg', upload_to='pic')
    name = models.CharField(max_length=50)


class Parties(models.Model):
    image = models.ImageField(default='parti.jpg', upload_to='pic')
    name = models.CharField(max_length=50)


class Planner(models.Model):
    image = models.ImageField(default='car.jpg', upload_to='pic')
    name = models.CharField(max_length=50)


class Tailor(models.Model):
    username = models.ForeignKey(UserRegister, on_delete=models.CASCADE, limit_choices_to={'category': 'tailor'})
    image = models.ImageField(default='tailor1.jpg', upload_to='pic')
    name = models.CharField(max_length=50)
    desc = models.CharField(max_length=500)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Catering(models.Model):
    username = models.ForeignKey(UserRegister, on_delete=models.CASCADE, limit_choices_to={'category': 'catering'})
    image = models.ImageField(default='tailor1.jpg', upload_to='pic')
    name = models.CharField(max_length=50)
    desc = models.CharField(max_length=500)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Entertainer(models.Model):
    username = models.ForeignKey(UserRegister, on_delete=models.CASCADE, limit_choices_to={'category': 'entertainer'})
    image = models.ImageField(default='tailor1.jpg', upload_to='pic')
    name = models.CharField(max_length=50)
    desc = models.CharField(max_length=500)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class AdminBooking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('nil', 'Nil'),
    ]
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, limit_choices_to={'status': 'confirmed'})
    booked_on = models.DateField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    # Relationships with Tailor, Catering, and Entertainer
    tailor = models.ForeignKey('Tailor', on_delete=models.CASCADE, null=True, blank=True)
    catering = models.ForeignKey('Catering', on_delete=models.CASCADE, null=True, blank=True)
    entertainer = models.ForeignKey('Entertainer', on_delete=models.CASCADE, null=True, blank=True)

    tailor_status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    caterer_status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    entertainer_status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def save(self, *args, **kwargs):
        # Set statuses to 'nil' if the services are not selected (None)
        if not self.tailor:
            self.tailor_status = 'nil'  # If no tailor, set status to 'nil'
        if not self.catering:
            self.caterer_status = 'nil'  # If no catering, set status to 'nil'
        if not self.entertainer:
            self.entertainer_status = 'nil'  # If no entertainer, set status to 'nil'

            # Collect all statuses excluding 'nil'
            active_statuses = [
                status for status in [self.tailor_status, self.caterer_status, self.entertainer_status]
                if status != 'nil'
            ]

            if all(status == 'confirmed' for status in active_statuses):
                self.status = 'confirmed'  # All booked services are confirmed
            elif any(status == 'cancelled' for status in active_statuses):
                self.status = 'pending'  # Any service is cancelled
            elif all(status == 'completed' for status in active_statuses):
                self.status = 'completed'  # All booked services are completed
            else:
                self.status = 'pending'  # Default to pending for other cases

        super().save(*args, **kwargs)

    def confirm_tailor(self):
        self.tailor_status = 'confirmed'
        self.save()

    def confirm_caterer(self):
        self.caterer_status = 'confirmed'
        self.save()

    def confirm_entertainer(self):
        self.entertainer_status = 'confirmed'
        self.save()

    def __str__(self):
        return f"Booking #{self.pk} - {self.status}"
