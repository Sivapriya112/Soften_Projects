from django.contrib import admin
from . models import *
# Register your models here.
admin.site.register(Events)
admin.site.register(Gallery)
admin.site.register(Catering)
admin.site.register(Entertainer)
admin.site.register(Parties)
admin.site.register(Resort)
admin.site.register(Stories)
admin.site.register(Planner)
admin.site.register(Tailor)
admin.site.register(PasswordReset)

@admin.register(UserRegister)
class UserRegisterAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'category', 'is_confirmed')
    search_fields = ('username', 'status')
    list_filter = ('category', 'is_confirmed')
    actions = ['confirm_registration']

    def confirm_registration(self, request, queryset):
        for obj in queryset:
            if obj.category != 'user':  # Ensure 'user' category doesn't need confirmation
                obj.is_confirmed = True
                obj.save()
        self.message_user(request, "Selected registrations have been confirmed.")

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user_details', 'phone', 'event', 'booking_date', 'status')
    list_filter = ('status', 'booking_date', 'refund_processed')
    search_fields = ('user_details__username', 'event__name')

@admin.register(AdminBooking)
class AdminBookingAdmin(admin.ModelAdmin):
    list_display = (
        'booking', 'booked_on', 'status'
    )
    list_filter = ('status', 'booking__booking_date')
    search_fields = ('booking_user_details__username', 'booking__event__name', 'booking__address', 'status')
    readonly_fields = ('booked_on',)

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploaded_at')
    search_fields = ('title',)
    list_filter = ('uploaded_at',)

@admin.register(Shorts)
class ShortsAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploaded_at')
    search_fields = ('title',)
    list_filter = ('uploaded_at',)