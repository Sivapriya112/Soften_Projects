from django.db import connection
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib import messages
from .forms import *
from .models import*
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator


# Create your views here.

def index(request):
    return render(request,'index.html')

def user_register(request):
    if request.method=="POST":
        a=request.POST['name']
        b=request.POST['phone']
        c=request.POST['email']
        d=request.POST['username']
        e=request.POST['password']
        if userregister.objects.filter(username=d).exists():
            return HttpResponse("Username already exists")
        else:
            userregister.objects.create(name=a,phone=b,email=c,username=d,password=e).save()
            return render(request,'login.html')
    else:
        return render(request,'user_register.html')

def developer_register(request):
    if request.method=="POST":
        a=request.POST['name']
        b=request.POST['phone']
        c=request.POST['email']
        d=request.POST['skills']
        e=request.POST['experience']
        f=request.POST['username']
        g=request.POST['password']
        if developerregister.objects.filter(username=d).exists():
            return HttpResponse("Developer already exists")
        else:
            developerregister.objects.create(name=a,phone=b,email=c,skills=d,experience=e,username=f,password=g).save()
            return redirect(developer_register)
    else:
        return render(request,'developer_register.html')


def login(request):
    if request.method == "POST":
        a = request.POST['username']
        b = request.POST['password']

        #  USER LOGIN
        try:
            data = userregister.objects.get(username=a)
            if data.password == b:
                request.session['user'] = a
                return redirect(user_home)
            else:
                return HttpResponse("Incorrect password for User")
        except:
            pass

        #  DEVELOPER LOGIN
        try:
            data = developerregister.objects.get(username=a)

            if data.password == b:

                if data.status == 'Accepted':

                    request.session['developer'] = a
                    request.session['developer_id'] = data.id

                    return redirect(developer_home)

                else:
                    return HttpResponse("Developer Not Accepted")

            else:
                return HttpResponse("Incorrect password for Developer")

        except:
            pass

        # ✅ ADMIN LOGIN
        if a == 'admin' and b == 'admin123':
            request.session['admin'] = a
            return redirect(admin_home)

        # ❌ IF NOTHING MATCHES
        return HttpResponse("Invalid username or password")

    return render(request, 'login.html')

def admin_home(request):
    return render(request,'admin_home.html')

def user_home(request):
    return render(request,'user_home.html')

def developer_home(request):

    developer_id = request.session['developer_id']

    return render(
        request,
        'developer_home.html',
        {
            'developer_id': developer_id
        }
    )

def logoutform(request):
    if 'user' in request.session and 'developer' in request.session and 'admin' in request.session:
        del request.session['user']
        del request.session['developer']
        del request.session['admin']
    return redirect(index)

def manage_developer(request):
    data=developerregister.objects.all()
    return render(request,'admin_view_manage_developer.html',{'data':data})

def accept_developer(request,d):
    data=developerregister.objects.get(pk=d)
    data.status='Accepted'
    data.save()
    return redirect(manage_developer)

def reject_developer(request,d):
    data=developerregister.objects.get(pk=d)
    data.status='Rejected'
    data.save()
    return redirect(manage_developer)

def create_project(request):

    if request.method == "POST":

        username = request.session['user']

        user = userregister.objects.get(username=username)

        title = request.POST['title']

        description = request.POST['description']

        budget = request.POST['budget']

        deadline = request.POST['deadline']


        # CATEGORY

        category_value = request.POST['category']

        other_category = request.POST.get('other_category')


        if category_value == "other":

            category_obj, created = Category.objects.get_or_create(
                category_name=other_category
            )

        else:

            category_obj = Category.objects.get(id=category_value)



        # CREATE PROJECT

        project = createproject.objects.create(

            user=user,

            title=title,

            description=description,

            category=category_obj,

            budget=budget,

            deadline=deadline

        )


        # TECHNOLOGY

        technology_ids = request.POST.getlist('technology')

        other_technology = request.POST.get('other_technology')


        # EXISTING TECHNOLOGIES

        for tech_id in technology_ids:

            tech = Technology.objects.get(id=tech_id)

            project.technologies.add(tech)


        # OTHER TECHNOLOGY

        if other_technology:

            tech_obj, created = Technology.objects.get_or_create(

                technology_name=other_technology

            )

            project.technology.add(tech_obj)


    return render(request,
                  'user_create_project.html',
                  {
                      'categories': Category.objects.all(),
                      'technologies': Technology.objects.all()
                  })


def admin_view_project(request):
    data=createproject.objects.all()
    return render(request,'admin_view_project.html',{'data':data})

def accept_project(request,d):
    data=createproject.objects.get(pk=d)
    data.status='Accepted'
    data.save()
    return redirect(admin_view_project)

def reject_project(request,d):
    data=createproject.objects.get(pk=d)
    data.status='Rejected'
    data.save()
    return redirect(admin_view_project)

def admin_view_manage_user(request):
    data=userregister.objects.all()
    return render(request,'admin_view_manage_user.html',{'data':data})

def admin_view_proposals(request):
    data=developerproposal.objects.all()
    return render(request,'admin_view_proposals.html',{'data':data})

def developer_view_project(request):
    username = request.session['developer']
    dev = developerregister.objects.get(username=username)

    data = createproject.objects.all()

    for i in data:
        proposal = developerproposal.objects.filter(
            project=i,
            developer=dev
        ).first()

        i.my_proposal = proposal  # attach proposal

    return render(request, 'developer_view_project.html', {'data': data})


def user_review_rating(request, id):

    username = request.session['user']

    user = userregister.objects.get(
        username=username
    )

    project = createproject.objects.get(id=id)

    proposal = developerproposal.objects.get(
        project=project
    )

    developer = proposal.developer

    if request.method == "POST":

        review = request.POST['review']

        rating = request.POST['rating']

        already = userreview.objects.filter(
            user=user,
            project=project
        ).exists()

        if already:
            return HttpResponse(
                "Review already submitted"
            )

        userreview.objects.create(
            user=user,
            developer=developer,
            project=project,
            review=review,
            rating=rating
        )

        return HttpResponse(
            "Review submitted successfully"
        )

    return render(
        request,
        'user_review_rating.html'
    )

from django.db.models import Avg, Count
def admin_view_review_rating(request):

    developers = developerregister.objects.annotate(
        avg_rating=Avg('userreview__rating'),
        total_reviews=Count('userreview')
    )
    return render(
        request,
        'admin_view_review_rating.html',
        {
            'developers': developers
        }
    )

def developer_profile(request):
        user=developerregister.objects.get(username=request.session['developer'])
        m=developerform(instance=user)
        print(m)
        if request.method=='POST':
            m=developerform(request.POST,request.FILES,instance=user)
            print("***************************")
            if m.is_valid():
                print("worked")
                print(m.is_valid())
                m.save()
                messages.success(request,'Profile Updated successfully')
                return redirect(developer_profile)
            else:
                messages.error(request,f'{m.errors}')
                return redirect(developer_profile)

        return render(request,'developer_profile.html',{'data':m})


def developer_portfolio(request):

    if request.method == "POST":

        username = request.session['developer']

        developer_obj = developerregister.objects.get(username=username)

        portfolio = developerportfolio.objects.create(
            developer=developer_obj,
            project_title=request.POST['project_title'],
            project_description=request.POST['project_description'],
            project_type=request.POST['project_type'],
            project_technology=request.POST['project_technology'],
            project_duration=request.POST['project_duration'],
            project_demo=request.POST['project_demo']
        )

        # multiple images
        images = request.FILES.getlist('images')

        for img in images:
            PortfolioImage.objects.create(
                portfolio=portfolio,
                image=img
            )

    return render(request, 'developer_portfolio.html')

def developer_view_portfolio(request):
    username = request.session['developer']
    developer_obj = developerregister.objects.get(username=username)
    data = developerportfolio.objects.filter(
        developer=developer_obj
    ).prefetch_related('images')
    return render(request, 'developer_view_portfolio.html', {'data': data})

def developer_update_portfolio(request,d):
   data=developerportfolio.objects.get(pk=d)
   m=updateportfolioform(instance=data)
   if request.method=='POST':
       m=updateportfolioform(request.POST,request.FILES,instance=data)
       if m.is_valid():
           m.save()
           return redirect(developer_view_portfolio)
   return render(request, 'developer_update_portfolio.html',{'data':m})


def developer_delete_portfolio(request,d):
    developerportfolio.objects.get(pk=d).delete()
    return redirect(developer_view_portfolio)

def developer_proposal_submit(request, d):
    if request.method == 'POST':
        username = request.session['developer']
        a = developerregister.objects.get(username=username)
        b = createproject.objects.get(pk=d)
        c = request.POST['project_proposal']
        d=request.POST['project_budget']
        developerproposal.objects.create(developer=a, project=b, project_proposal=c,project_budget=d).save()
        return render(request, 'developer_proposal_submit.html')

    return render(request, 'developer_proposal_submit.html', {'project_id': d})

# def user_view_proposal(request):
#     username = request.session['user']
#     a = userregister.objects.get(username=username)
#     createproject1=createproject.objects.get(user=a)
#     data=developerproposal.objects.filter(project=createproject1)
#     return render(request,'user_view_proposals.html',{'data':data})
def user_view_proposal(request):
    username = request.session['user']

    data = developerproposal.objects.filter(
        project__user__username=username
    )

    return render(request, 'user_view_proposals.html', {'data': data})

def accept_proposal(request, d):
    selected = developerproposal.objects.get(pk=d)
    project = selected.project

    #  Accept selected proposal
    selected.project_status = 'Accepted'
    selected.save()

    # Reject all other proposals for same project
    developerproposal.objects.filter(project=project)\
        .exclude(pk=d)\
        .update(project_status='Rejected')

    #  UPDATE PROJECT STATUS HERE
    project.status = 'assigned'
    project.save()

    return redirect(user_view_proposal)

def reject_proposal(request, d):
    data = developerproposal.objects.get(pk=d)

    if data.project_status == 'Accepted':
        messages.success(request, 'Cannot reject accepted proposal')
        return redirect(user_view_proposal)

    data.project_status = 'Rejected'
    data.save()

    return redirect(user_view_proposal)

# def developer_view_acceptedprojects(request):
#     dev=developerregister.objects.get(username=request.session['developer'])
#     data = developerproposal.objects.filter(developer=dev,project_status='Accepted')
#     return render(request,'developer_view_acceptedprojects.html',{'data':data})
def developer_view_acceptedprojects(request):
    dev = developerregister.objects.get(
        username=request.session['developer']
    )

    data = developerproposal.objects.filter(
        developer=dev,
        project_status__in=['Accepted', 'completed']
    )

    return render(
        request,
        'developer_view_acceptedprojects.html',
        {'data': data}
    )

def developer_view_rejectedprojects(request):
    dev = developerregister.objects.get(username=request.session['developer'])
    data=developerproposal.objects.filter(developer=dev,project_status='Rejected')
    return render(request,'developer_view_rejectedprojects.html',{'data':data})

# def developer_worksubmission(request,d):
#     if request.method=="POST":
#         a = developerproposal.objects.get(pk=d)
#         pro=createproject.objects.get(pk=a.project.id)
#         print(pro,a.project.id)
#         username=request.session['developer']
#         b = developerregister.objects.get(username=username)
#         c= request.FILES['file']
#         d = request.POST['description']
#         worksubmission.objects.create(project=pro, developer=b, file=c, description=d).save()
#         return render(request,'developer_worksubmission.html')
#     return  render(request,'developer_worksubmission.html')



def developer_view_uploadedprojects(request):
    data = worksubmission.objects.all()
    return render(request,'developer_view_uploadedprojects.html',{'data':data})

# def user_view_uploadedproject(request):
#     username = request.session['user']
#     a = userregister.objects.get(username=username)
#     createproject1=createproject.objects.filter(user=a)
#     data = worksubmission.objects.filter(project=createproject1)
#     return render(request,'user_view_uploadedproject.html',{'data':data})

def user_view_uploadedproject(request, d):

    proposal = developerproposal.objects.get(pk=d)

    data = worksubmission.objects.filter(
        project=proposal.project,
        developer=proposal.developer
    )

    return render(request, 'user_view_uploadedproject.html', {'data': data,'proposal':proposal})


from django.shortcuts import render, redirect
from .models import Message, createproject

def chat(request, project_id):
    project = createproject.objects.get(id=project_id)

    user = None
    developer = None

    if 'user' in request.session:
        user = userregister.objects.get(username=request.session['user'])

    if 'developer' in request.session:
        developer = developerregister.objects.get(username=request.session['developer'])

    # SEND MESSAGE
    if request.method == "POST":
        text = request.POST.get("message")

        if text:
            Message.objects.create(
                project=project,
                sender_user=user if user else None,
                sender_developer=developer if developer else None,
                message=text
            )
        return redirect(chat, project_id=project_id)

    messages = Message.objects.filter(project=project).order_by('timestamp')

    return render(request, "chat.html", {
        "project": project,
        "messages": messages,
        "user": user,
        "developer": developer
    })

def update_progress(request, d):
    if 'developer' not in request.session:
        return redirect('login')

    project = createproject.objects.get(id=d)

    try:
        dev = developerproposal.objects.get(
            project=project,
            project_status='Accepted'
        )
    except developerproposal.DoesNotExist:
        messages.error(request,'No accepted developer found')
        return redirect(view_more_project,d)
    except developerproposal.MultipleObjectsReturned:
        messages.error(request,'Multiple accepted developer found')
        return redirect(view_more_project,d)

    developer = developerregister.objects.get(
        username=request.session['developer']
    )

    # ✅ Only assigned developer
    if dev.developer != developer:
        return HttpResponse("Not allowed")

    if request.method == "POST":
        progress_value = request.POST.get("progress")

        if progress_value:
            new_progress = int(progress_value)

            # ✅ Prevent decreasing
            if new_progress >= project.progress and new_progress <= 100:
                project.progress = new_progress
                dev.progress = new_progress

                # ✅ Status update
                if new_progress == 100:
                    project.status = "completed"
                    dev.project_status = "completed"
                elif new_progress > 0:
                    project.status = "in progress"

                project.save()
                dev.save()

        return redirect(developer_view_acceptedprojects)

    return render(request, "update_progress.html", {"project": project})

# def update_progress(request, d):
#     project = createproject.objects.get(id=d)
#     dev=developerproposal.objects.get(project=project)
#
#     # Only developer allowed
#     if 'developer' not in request.session:
#         return redirect('login')
#
#     if request.method == "POST":
#         progress_value = request.POST.get("progress")
#
#         if progress_value:
#             new_progress = int(progress_value)
#
#             # ✅ Prevent decreasing
#             if new_progress >= project.progress and new_progress <= 100:
#                 project.progress = new_progress
#                 dev.progress = new_progress
#
#                 # Optional: update status
#                 if new_progress == 100:
#                     project.status = "completed"
#                 elif new_progress > 0:
#                     project.status = "in progress"
#
#                 project.save()
#                 dev.save()
#
#         return redirect(developer_view_acceptedprojects)
#
#     return render(request, "update_progress.html", {"project": project})

def user_view_updateprogress(request,d):
    project = developerproposal.objects.get(pk=d)

    # Only user allowed
    if 'user' not in request.session:
        return redirect('login')

    return render(request, "user_view_updateprogress.html", {"project": project})
import razorpay

# def user_advance_pay(request,id):
#     amount = 5000
#     order_currency = 'INR'
#     client = razorpay.Client(
#         auth=("rzp_test_SROSnyInFv81S4", "WIWYANkTTLg7iGbFgEbwj4BM"))
#
#     payment = client.order.create({'amount': amount, 'currency': 'INR', 'payment_capture': '1'})
#     return render(request, "user_advance_pay.html")

def developer_worksubmission(request, d):
    proposal = developerproposal.objects.get(pk=d)
    project = proposal.project

    # Check login
    if 'developer' not in request.session:
        return redirect('login')

    developer = developerregister.objects.get(
        username=request.session['developer']
    )

    # ✅ Only assigned developer
    if proposal.developer != developer:
        return HttpResponse("You are not allowed to submit this work")

    # ✅ Advance payment check (simple & clean)
    if proposal.advance_status != 'paid':
        return redirect(advancepay_notdone_popupmessage)

    # ✅ Prevent multiple submissions
    if worksubmission.objects.filter(project=project).exists():
        return HttpResponse("work_submitted_alert")

    if request.method == "POST":
        file = request.FILES.get('file')
        description = request.POST.get('description')

        if not file:
            return HttpResponse("Please upload a file")

        worksubmission.objects.create(
            project=project,
            developer=developer,
            file=file,
            description=description,
            upload_status='submitted'
        )

        project.status = 'submitted'
        project.save()

        proposal.project_status = 'submitted'
        proposal.save()

        return redirect(view_more_project,d)

    return render(request, 'developer_worksubmission.html', {"project": project})

def user_advance_pay(request, id):
    amount = 3000*100
    client = razorpay.Client(
        auth=("rzp_test_SROSnyInFv81S4", "WIWYANkTTLg7iGbFgEbwj4BM"))

    payment = client.order.create({
        'amount': amount,
        'currency': 'INR',
        'payment_capture': '1'
    })

    return render(request, "user_advance_pay.html", {
        "payment": payment,
        "id": id
    })

from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def pay_success(request,id):
    proposal = developerproposal.objects.get(id=id)
    # insert payment amount
    proposal.advance_pay = 3000  # or whatever
    proposal.advance_status = 'paid'
    proposal.save()
    return render(request, "pay_success.html", {"payment_success": True})

def advancepay_notdone_popupmessage(request):
    return render(request, "advancepay_notdone_popupmessage.html")

def work_submitted_alert(request):
    return render(request, "work_submitted_alert.html")

def view_more_project(request,d):
    data = developerproposal.objects.get(pk=d)
    return render(request, "view_more_project.html", {"data": data})

def user_view_ownprojects(request):
    if 'user' not in request.session:
        return redirect('login')

    user = userregister.objects.get(
        username=request.session['user']
    )

    data = createproject.objects.filter(user=user)

    return render(request, "user_view_ownprojects.html", {"data": data})

import razorpay
from django.shortcuts import render, redirect
from .models import payment, developerproposal

def user_final_pay(request, id):

    proposal = developerproposal.objects.get(id=id)
    project = proposal.project

    # ✅ Allow only after submission
    if proposal.project_status != 'submitted':
        return HttpResponse("Final payment not allowed yet")

    # ✅ Check advance payment
    if proposal.advance_status != 'paid':
        return HttpResponse("Advance payment not completed")

    # ✅ Prevent duplicate final payment
    if proposal.final_payment_status == 'paid':
        return HttpResponse("Final payment already completed")

    # ✅ Calculate balance amount
    # ✅ Calculate balance amount
    total_amount = int(proposal.project_budget)
    print("budget amount",total_amount)

    # ✅ Admin commission percentage
    admin_percentage = 10

    # ✅ Admin commission amount
    admin_commission = (total_amount * admin_percentage) // 100

    # ✅ Developer amount after commission
    developer_amount = total_amount - admin_commission

    # ✅ SAVE commission values
    proposal.admin_commission = admin_commission
    proposal.developer_amount = developer_amount
    proposal.save()

    AdminCommission.objects.create(
        project=project,
        developer=proposal.developer,
        total_amount=total_amount,
        admin_amount=admin_commission,
        developer_amount=developer_amount
    )

    advance_amount = 3000
    print(total_amount)
    balance_amount = total_amount - advance_amount
    print(balance_amount)

    if balance_amount <= 0:
        return HttpResponse("Invalid balance amount")

    amount_in_paisa = balance_amount * 100

    client = razorpay.Client(
        auth=("rzp_test_SROSnyInFv81S4", "WIWYANkTTLg7iGbFgEbwj4BM")
    )

    order = client.order.create({
        'amount': amount_in_paisa,
        'currency': 'INR',
        'payment_capture': '1'
    })

    # ✅ Save payment record
    pay = payment.objects.create(
        project=project,
        user=project.user,
        amount=balance_amount,
        payment_type='final',
        razorpay_order_id=order['id']
    )

    return render(request, "user_final_pay.html", {
        "order": order,
        "proposal": proposal,
        "payment": pay,
        "total_amount": total_amount,
        "advance_amount": advance_amount,
        "balance_amount": balance_amount
    })

@csrf_exempt
def final_pay_success(request):

    if request.method == "POST":

        order_id = request.POST.get('razorpay_order_id')
        payment_id = request.POST.get('razorpay_payment_id')

        try:
            pay = payment.objects.get(
                razorpay_order_id=order_id,
                payment_type='final'
            )

            # ✅ Update payment
            pay.razorpay_payment_id = payment_id
            pay.payment_status = 'paid'
            pay.save()

            # ✅ Update proposal
            proposal = developerproposal.objects.get(project=pay.project)

            proposal.final_payment_status = 'paid'
            proposal.project_status = 'completed'
            proposal.progress = 100
            proposal.save()

            # ✅ Update project
            project = pay.project

            project.status = 'completed'
            project.progress = 100
            project.save()

            # ✅ Enable download
            worksubmission.objects.filter(
                project=project
            ).update(payment_status='paid')

            return render(
                request,
                "pay_success.html",
                {"payment_success": True}
            )

        except payment.DoesNotExist:

            return HttpResponse("Invalid payment")

    return HttpResponse("Invalid Request")

def developer_view_review_rating(request):

    dev = developerregister.objects.get(
        username=request.session['developer']
    )

    data = userreview.objects.filter(developer=dev)

    return render(
        request,
        'developer_view_review_rating.html',
        {'data': data}
    )

from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

from .models import userregister, developerregister, PasswordReset


def forgot_password(request):

    if request.method == 'POST':

        email = request.POST.get('email')

        user = None
        user_type = None

        # Check user table
        if userregister.objects.filter(email=email).exists():

            user = userregister.objects.get(email=email)
            user_type = 'user'

        # Check developer table
        elif developerregister.objects.filter(email=email).exists():

            user = developerregister.objects.get(email=email)
            user_type = 'developer'

        else:
            messages.error(request, "Email not registered")
            return redirect(forgot_password)

        # Delete old tokens
        PasswordReset.objects.filter(email=email).delete()

        # Create new token
        reset_obj = PasswordReset.objects.create(
            email=email,
            user_type=user_type
        )

        token = reset_obj.token

        reset_link = f"http://127.0.0.1:8000/reset-password/{token}/"

        subject = "Reset Password"

        message = f"""
Hello {user.name},

Click the link below to reset your password:

{reset_link}
"""
        try:

            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
        except Exception as e:
            print(e)

        messages.success(request, "Reset link sent to your email")
        return redirect(login)

    return render(request, 'forgot_password.html')

from django.contrib.auth.hashers import make_password
from .models import PasswordReset


def reset_password(request, token):

    try:
        reset_obj = PasswordReset.objects.get(token=token)

    except PasswordReset.DoesNotExist:

        messages.error(request, "Invalid reset link")
        return redirect('forgot_password')

    # Get user
    if reset_obj.user_type == 'user':

        user = userregister.objects.get(email=reset_obj.email)

    else:

        user = developerregister.objects.get(email=reset_obj.email)

    if request.method == 'POST':

        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password == confirm_password:

            # encrypted password
            user.password = make_password(password)

            user.save()

            # delete token after use
            reset_obj.delete()

            messages.success(request, "Password reset successful")
            return redirect('login')

        else:

            messages.error(request, "Passwords do not match")

    return render(request, 'reset_password.html')


def browse_freelancers(request):
    data = developerregister.objects.filter( status='Accepted')
    print(data)
    return render(request,'browse_freelancers.html',{'data': data})

def user_view_portfolio(request,id):
    developer = developerregister.objects.get(pk=id)
    data = developerportfolio.objects.filter(developer=developer)
    return render(request,'user_view_portfolio.html',{'data':data})

def start_chat(request, id):

    student = userregister.objects.get(
        username=request.session['user']
    )

    dev = developerportfolio.objects.get(id=id)
    developer= developerregister.objects.get(username=dev.developer.username)

    room, created = ChatRoom.objects.get_or_create(
        student=student,
        developer=developer
    )

    return redirect(f'/chatpage/{room.id}')

def chat_page(request, id):

    room = ChatRoom.objects.get(id=id)
    print(room)

    messages = Message.objects.filter(
        room=room
    ).order_by('timestamp')
    print(messages)
    return render(request, 'chat1.html', {
        'room': room,
        'messages': messages
    })

def send_message(request, id):

    print("FUNCTION WORKING")

    if request.method == "POST":

        room = ChatRoom.objects.get(id=id)

        text = request.POST.get('message')

        print(text)

        Message.objects.create(
            room=room,
            sender=request.session['user'],
            message=text
        )

        print("MESSAGE SAVED")

    return redirect(f'/chatpage/{id}/')

def developer_chat_list(request):

    developer = developerregister.objects.get(
        username=request.session['developer']
    )

    rooms = ChatRoom.objects.filter(
        developer=developer
    )

    return render(request,
                  'developer_chat_list.html',
                  {'rooms': rooms})

def developer_chat_page(request, id):

    room = ChatRoom.objects.get(id=id)

    messages = Message.objects.filter(
        room=room
    ).order_by('timestamp')

    return render(request,
                  'developer_chat.html',
                  {
                      'room': room,
                      'messages': messages
                  })

def developer_send_message(request, id):

    if request.method == "POST":

        room = ChatRoom.objects.get(id=id)

        text = request.POST.get('message')

        Message.objects.create(
            room=room,
            sender=request.session['developer'],
            message=text
        )

    return redirect(f'/developerchat/{id}/')

def admin_income(request):

    data = AdminCommission.objects.all()

    total_income = 0

    for i in data:
        total_income += i.admin_amount

    return render(request,
                  'admin_income.html',
                  {
                      'data': data,
                      'total_income': total_income
                  })
from django.db.models import Sum

def admin_view_commission(request):

    month = request.GET.get('month')

    data = AdminCommission.objects.all()

    # Filter by selected month
    if month:
        data = data.filter(created_at__month=month)

    # Total project amount
    total_amount = data.aggregate(
        Sum('total_amount')
    )['total_amount__sum'] or 0

    # Total admin income
    total_admin = data.aggregate(
        Sum('admin_amount')
    )['admin_amount__sum'] or 0

    return render(
        request,
        'admin_view_commission.html',
        {
            'data': data,
            'total_amount': total_amount,
            'total_admin': total_admin,
            'selected_month': month
        }
    )

def user_view_all_projects(request):
    projects = createproject.objects.all()
    search = request.GET.get('search')
    category = request.GET.get('category')
    technology = request.GET.get('technology')
    budget = request.GET.get('budget')

    # SEARCH
    if search:

        title_projects = createproject.objects.filter(
            project_title__icontains=search
        )

        description_projects = createproject.objects.filter(
            project_description__icontains=search
        )

        projects = title_projects | description_projects

    # CATEGORY FILTER
    if category:
        projects = projects.filter(category=category)

    # TECHNOLOGY FILTER
    if technology:
        projects = projects.filter(technologies=technology)

    # BUDGET FILTER
    if budget:
        projects = projects.filter(budget__lte=budget)

    context = {
        'projects': projects
    }

    return render(request,
                  'user_view_all_projects.html',
                  context)

from django.shortcuts import render,redirect

from .models import *


# ADD CATEGORY

def add_category(request):

    if request.method == "POST":

        category_name = request.POST['category']


        # CHECK EXISTING CATEGORY

        if not Category.objects.filter(
                category_name=category_name
        ).exists():

            Category.objects.create(
                category_name=category_name
            )

        return redirect(add_category)


    categories = Category.objects.all()

    context = {

        'categories': categories
    }

    return render(
        request,
        'admin_add_category.html',
        context
    )



# ADD TECHNOLOGY

def add_technology(request):

    if request.method == "POST":

        technology_name = request.POST['technology']


        # CHECK EXISTING TECHNOLOGY

        if not Technology.objects.filter(
                technology_name=technology_name
        ).exists():

            Technology.objects.create(
                technology_name=technology_name
            )

        return redirect(add_technology)


    technologies = Technology.objects.all()

    context = {

        'technologies': technologies
    }

    return render(
        request,
        'admin_add_technology.html',
        context
    )

from django.db.models import Avg

def developer_avg_rating(request, id):
    developer = developerregister.objects.get(id=id)
    reviews = userreview.objects.filter(
        developer=developer
    )
    avg_rating = reviews.aggregate(
        Avg('rating')
    )
    return render(request,
                  'developer_avg_rating.html',
                  {
                      'developer': developer,
                      'reviews': reviews,
                      'avg_rating': avg_rating
                  })