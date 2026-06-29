"""
URL configuration for event project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from app1 import views

urlpatterns = [
    path("admin/", admin.site.urls),
    # index
    path("", views.index),
    path("about", views.about),
    path("contact", views.contact),
    path("stories", views.stories),
    path("service", views.service),
    path("resorts", views.resorts),
    path("login", views.login),
    path("register", views.register),
    path("account", views.account),
    path("catering", views.catering),
    # path("booking",views.booking),
    path("testimonial", views.testimonial),
    path("gallery", views.gallery),
    path("video_gallery", views.video_gallery),
    path("shorts", views.shorts),
    path("corp", views.corp),
    path("beach", views.beach),
    path("stitching", views.stitching),
    path("wed", views.wed),
    path("parties", views.parties),
    path("music", views.music),
    # user
    path("uabout", views.uabout),
    path("ustories", views.ustories),
    path("uservice", views.uservice),
    path("uresorts", views.uresorts),
    path('booking_cancel/<int:booking_id>/', views.booking_cancel, name='booking_cancel'),
    path('booking', views.booking, name='booking'),

    path("utestimonial", views.utestimonial),
    path("ugallery", views.ugallery),
    path("uvideo", views.uvideo),
    path("ushorts", views.ushorts),
    path("ucorp", views.ucorp),
    path("ubeach", views.ubeach),
    path("ustitching", views.ustitching),
    path("uwed", views.uwed),
    path("uparties", views.uparties),
    path("umusic", views.umusic),
    path("ucontact", views.ucontact),
    path("ucatering", views.ucatering),
    path("profile", views.profile),
    # admin
    path("ad_account", views.ad_account),
    path("ad_stories", views.ad_stories),
    path("ad_service", views.ad_service),
    path("ad_resorts", views.ad_resorts),
    path("ad_bookings", views.ad_bookings),
    path('update-payment/<int:booking_id>/', views.update_total_payment, name='update_total_payment'),
    path('booking/confirm/<int:booking_id>/', views.confirm_booking, name='confirm_booking'),
    path('booking/cancel/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('booking/completed/<int:booking_id>/', views.completed_booking, name='completed_booking'),
    path('booking/paid/<int:booking_id>/', views.paid_booking, name='paid_booking'),
    path('refund/<int:booking_id>/', views.refund_payment, name='refund_payment'),
    path('refund_success', views.refund_success, name='refund_success'),
    path('admin/booking/cancel/<int:booking_id>/', views.cancel_admin_booking, name='cancel_admin_booking'),

    path("ad_gallery", views.ad_gallery),
    path("ad_videos", views.ad_videos),
    path("ad_shorts", views.ad_shorts),
    path("ad_stitching", views.ad_stitching),
    path("ad_wed", views.ad_wed),
    path("ad_parties", views.ad_parties),
    path("ad_music", views.ad_music),
    path("ad_profile", views.ad_profile),
    path("user_details", views.user_details),
    path("user/confirm/<int:d>/", views.user_confirm, name='user_confirm'),

    path("logout", views.logout),
    path("payment", views.payment),
    path("success", views.success),
    path("forgot", views.forgot_password),
    path("reset/<token>", views.reset_password),
    path('delete/<int:d>', views.resort_delete),
    path('update/<int:d>', views.resort_update),
    path('update_gallery/<int:d>', views.gallery_update),
    path('update_video/<int:d>', views.video_update),
    path('update_shorts/<int:d>', views.shorts_update),
    path('delete1/<int:d>', views.stories_delete),
    path('delete2/<int:d>', views.planner_delete),
    path('delete3/<int:d>', views.parties_delete),
    path('delete_music/<int:d>', views.music_delete),
    path('delete5/<int:d>', views.user_delete),
    path('delete_gallery/<int:d>', views.galley_delete),
    path('delete_video/<int:d>', views.video_delete),
    path('delete_shorts/<int:d>', views.shorts_delete),
    # tailor
    path("tailor_home", views.tailor_home),
    path('tailor_booking', views.tailor_booking, name='tailor_booking'),
    path('tailor_confirm/<int:booking_id>/', views.tailor_confirm, name='tailor_confirm'),
    path('tailor_ignore/<int:booking_id>/', views.tailor_ignore, name='tailor_ignore'),
    path('tailor_complete/<int:booking_id>/', views.tailor_complete, name='tailor_complete'),
    path("tailor_profile", views.tailor_profile),
    # entertainment
    path("enter_home", views.enter_home),
    path('entertainer_booking', views.entertainer_booking, name='entertainer_booking'),
    path('enter_confirm/<int:booking_id>/', views.enter_confirm, name='enter_confirm'),
    path('enter_ignore/<int:booking_id>/', views.enter_ignore, name='enter_ignore'),
    path('enter_complete/<int:booking_id>/', views.enter_complete, name='enter_complete'),
    path("enter_profile", views.enter_profile),
    # catering
    path("cater_home", views.cater_home),
    path('cater_booking', views.cater_booking),
    path('cater_confirm/<int:booking_id>/', views.cater_confirm, name='cater_confirm'),  # Confirm booking
    path('cater_ignore/<int:booking_id>/', views.cater_ignore, name='cater_ignore'),  # Cancel booking
    path('cater_complete/<int:booking_id>/', views.cater_complete, name='cater_complete'),  # Complete booking
    path("cater_profile", views.cater_profile),
    path("terms", views.terms),
    path('uterms', views.uterms),

    path('admin_booking', views.admin_booking),
    path('change_tailor/<int:booking_id>/', views.change_tailor, name='change_tailor'),
    path('change_caterer/<int:booking_id>/', views.change_caterer, name='change_caterer'),
    path('change_entertainer/<int:booking_id>/', views.change_entertainer, name='change_entertainer'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
