"""softenproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from webdevelopersite import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('index',views.index),
    path('userregister',views.user_register),
    path('developerregister',views.developer_register),
    path('login',views.login),
    path('logout',views.logoutform),
    path('adminhome',views.admin_home),
    path('userhome',views.user_home),
    path('developerhome',views.developer_home),
    path('managedeveloper',views.manage_developer),
    path('acceptdeveloper/<int:d>',views.accept_developer),
    path('rejectdeveloper/<int:d>',views.reject_developer),
    path('createproject',views.create_project),
    path('adminviewproject',views.admin_view_project),
    path('acceptproject/<int:d>',views.accept_project),
    path('rejectproject/<int:d>',views.reject_project),
    path('manageuser',views.admin_view_manage_user),
    path('adminviewproposals',views.admin_view_proposals),
    path('developerviewproject',views.developer_view_project),
    path('userreviewrating/<int:id>',views.user_review_rating, name='userreviewrating'),
    path('adminreviewrating',views.admin_view_review_rating),
    path('developerprofile',views.developer_profile),
    path('developerportfolio',views.developer_portfolio),
    path('developerviewportfolio',views.developer_view_portfolio),
    path('developerupdateportfolio/<int:d>',views.developer_update_portfolio),
    path('developerdeleteportfolio/<int:d>',views.developer_delete_portfolio),
    path('developerproposalsubmit/<int:d>',views.developer_proposal_submit),
    path('userviewproposal',views.user_view_proposal),
    path('acceptproposal/<int:d>',views.accept_proposal),
    path('rejectproposal/<int:d>',views.reject_proposal),
    path('developerviewacceptedprojects',views.developer_view_acceptedprojects),
    path('developerviewrejectedprojects',views.developer_view_rejectedprojects),
    path('developerworksubmission/<int:d>',views.developer_worksubmission),
    path('developerviewuploadedprojects',views.developer_view_uploadedprojects),
    path('userviewuploadedproject/<int:d>',views.user_view_uploadedproject),
    path('chat/<int:project_id>/',views.chat),
    # path('userchat/<int:d>/', views.user_chat),
    # path('developerchat/<int:d>/', views.developer_chat),
    # path('get-messages/<int:d>/', views.get_messages, name='get_messages'),
    path('updateprogress/<int:d>',views.update_progress),
    path('userviewupdateprogress/<int:d>',views.user_view_updateprogress),
    path('useradvancepay/<int:id>',views.user_advance_pay),
    path('paysuccess/<int:id>',views.pay_success,name='paysuccess'),
    path('advancepaynotdonepopupmessage',views.advancepay_notdone_popupmessage),
    path('worksubmittedalert',views.work_submitted_alert),
    path('viewmoreproject/<int:d>',views.view_more_project),
    path('userviewownprojects',views.user_view_ownprojects),
    path('userfinalpay/<int:id>', views.user_final_pay),
    path('finalpaysuccess/', views.final_pay_success,name='final_pay_success'),
    path('developerviewreviewrating',views.developer_view_review_rating),
    path('forgot-password', views.forgot_password, name='forgot_password'),
    path('reset-password/<uidb64>/<token>',views.reset_password,name='reset_password'),
    path('browsefreelancers',views.browse_freelancers),
    path('userviewportfolio/<int:id>',views.user_view_portfolio),
    path('startchat/<int:id>',views.start_chat),
    path('chatpage/<int:id>/',views.chat_page),
    path('sendmessage/<int:id>/',views.send_message,name='sendmessage'),
    path('developerchatlist', views.developer_chat_list),
    path('developerchat/<int:id>/', views.developer_chat_page),
    path('developersendmessage/<int:id>/',views.developer_send_message),
    path('adminviewcommission',views.admin_view_commission),
    path('userviewallprojects',views.user_view_all_projects),
    path('addcategory',views.add_category,name='add_category'),
    path('addtechnology',views.add_technology,name='add_technology'),
    path('developeravgrating/<int:id>',views.developer_avg_rating),
]
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
