"""
URL configuration for website project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from app1 import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('register/', views.register),
    path('login/', views.login),
    path('logout/', views.logout),
    path('user_home/', views.user_home),
    path('worker_home/', views.worker_home),
    path('worker/update-status/', views.update_worker_status, name='update_worker_status'),
    path('worker_detail/<int:id>', views.worker_detail),
    path('book_worker/<int:id>/', views.book_worker),
    path('update_booking/<int:booking_id>/<str:action>/', views.update_booking),
    path('upload_document/',views.upload_document),
    path('admin_home/', views.admin_home),
    path('verify_worker/<int:id>/', views.verify_worker),
    path('reject_worker/<int:id>/', views.reject_worker),
    path('submit_complaint/<int:worker_id>/', views.submit_complaint),
    path('terminate_worker/<int:worker_id>/', views.terminate_worker),
    path('warn_worker/<int:worker_id>/', views.warn_worker),
    path('complaints/', views.complaints),
    path('view_complaints/<int:worker_id>/<str:username>/',views.view_complaints),
    path('booking_detail/<int:id>/', views.booking_detail),
    path('update_work_status/<int:id>/', views.update_work_status),
    path('collect_cash/<int:id>/', views.collect_cash),
    path('payment/<int:id>/', views.payment),
    path('payment_success/', views.payment_success),
    path('submit_rating/<int:id>/',views.submit_rating),
    path('booking_detail_user/', views.booking_detail_user),
    path('booking_detail_worker/',views.booking_detail_worker),
    path('booking_detail_admin/<int:worker_id>/', views.booking_detail_admin),




]
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
