"""
URL configuration for concertbooking project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from app import views

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),


    path('', views.main_home),
    path('login', views.login),

    path('userregister', views.registration_user),
    path('managerregister', views.registration_manager),

    path('userhome', views.user_home),
    path('adminhome', views.admin_home),
    path('managerhome', views.manager_home),
    path('addevent', views.add_event),
    path('about', views.about),
    path('viewevent', views.view_event),
    path('vieweventadmin', views.view_event_admin),

    path('concertview/<int:d>', views. concertview),
    path('demo/<int:d>', views.demo),
    path('success_page', views.success_page),


    path('contact', views.contact),
    path('view_event_2/<int:d>', views. view_event_2),
    path('admindis/<int:d>', views.admindis),


    path('logout', views.logout),

    path('userconcerts', views.concert_user),

    path('category/<int:d>', views.category),
    path('amount1/<int:d>', views.amount1),


    path('details/<int:d>/<int:amount>/<int:no_tickets>', views.details),
    path('pay/<int:amount>',views.pay,name='pay'),

    path('viewuser', views.view_user),
    path('viewmessage', views.View_contact),
    path('viewmanager', views.view_manager),

    path('rejectmanager/<int:d>', views.reject_manager),
    path('rejectevent/<int:d>', views.reject_event),

    path('deleteevent/<int:d>', views.delete_event),
    path('updateevent/<int:d>', views.update_event),
    path('acceptmanager/<int:d>', views.accept_manager),
    path('acceptevent/<int:d>', views.accept_event),

    path('eventaccepted', views.event_accepted_by_admin),
    path('manageraccepted', views.manager_accepted_by_admin),

    path('forgot', views.forgot_password, name="forgot"),
    path('reset/<token>', views.reset_password, name='reset_password'),

    path('concertview/<int:d>', views.concertview),
    path('admin_order_details', views.admin_orders, name='admin_order_details'),
    path('manager_order_details', views.manager_orders, name='manager_order_details'),
    path('admin_order_update/<int:d>', views.adminorderupdate),

    path('user_recent_orders',views.userrecentorders, name='user_recent_orders')

]
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)