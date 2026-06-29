from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import os
import razorpay
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from datetime import datetime
from django.core.mail import send_mail



# Create your views here.


def main_home(request):
    return render(request, 'Mainhome_project.html')
def login(request):
    return render(request, 'Login.html')

def login1(request):
    return render(request, 'meera.html')

def home(request):
    return render(request, 'verthe.html')


def user_home(request):
    if 'id' in request.session:
        user =Register_user.objects.get(Email=request.session['id'])
        print(user)
        data =Events.objects.all()
        return render(request, 'User_home.html',{'data': user, 'data1': data})
    return redirect(login)

def admin_home(request):
    if 'id1' in request.session:
        return render(request, 'Admin_home.html')
    return redirect(login)
def manager_home(request):
    if 'id2' in request.session:
        return render(request, 'Manager_home.html')
    return redirect(login)


def contact(request):
    if request.method=='POST':
        name=request.POST['n1']
        email= request.POST['n2']
        phone = request.POST['n3']
        issue= request.POST['n4']
        eventname= request.POST['n5']
        query = request.POST['n6']
        details= User_contact.objects.create(Username=name,Email=email,Phoneno=phone,issue=issue,eventname=eventname,query=query)
        details.save()
        messages.success(request, 'Data Saved')
        return redirect(contact)
        return render(request, 'user_Contact.html')
    return render(request, 'user_Contact.html')
def View_contact(request):
    if 'id1' in request.session:
        details = User_contact.objects.all()
        return render(request, 'admin_View_message.html', {'data': details})
    redirect(login)



def login(request):
    if request.method == 'POST':
        u = request.POST['email']
        p = request.POST['password']
        try:
            data = Register_user.objects.get(Email=u)
            if p == data.Password:
                request.session['id'] = u  # session creation using id,id must be different
                return redirect(user_home)
        except Exception:
            try:
                data1 = Register_manager.objects.get(Email=u)
                if data1.Status == 'ACCEPTED':
                    if p == data1.Password:
                        request.session['id2'] = u  # session creation using id,id must be different
                        return redirect(manager_home)
                    else:
                        messages.error(request,'Incorrect Password')
                else:
                    messages.error(request,'Permission needed to login...')
            except Exception:
                if u == 'admin@gmail.com' and p == 'admin':
                    request.session['id1'] = u
                    return redirect(admin_home)
                else:
                    messages.error(request,'Incorrect Password')
            messages.error(request,'Incorrect Username')
    return render(request, 'project_login.html')
def logout(request):
    if 'id' in request.session or 'id1' in request.session or 'id2' in request.session:
        request.session.flush()
        return redirect(login)
    return redirect(login)
def registration_user(request):
    if request.method=='POST':
        name=request.POST['n1']
        email= request.POST['n2']
        phone = request.POST['n3']
        password = request.POST['n4']
        cpassword = request.POST['n5']
        if password==cpassword:
            if Register_user.objects.filter(Email=email).exists():
                messages.info(request, "Email already Registered", extra_tags="signup")
                return redirect(registration_user)
            else:
                val =Register_user.objects.create(Username=name,Email=email,Phoneno=phone,Password=password)
                val.save()
                messages.info(request, "Registered Successfully", extra_tags="signup")
                send_mail('Registration Successful',
                          f'{name} Your CONCERTBOOKING Account Has Been Successfully Registered. \nTHANK YOU For Registering',
                          'settings.EMAIL_HOST_USER', [email], fail_silently=False)
                return redirect(login)
        else:
            messages.info(request, "Password doesn't match", extra_tags="signup")
            return redirect(registration_user)

    return render(request, 'Registration_user.html')


def registration_manager(request):
    if request.method=='POST':
        name=request.POST['n1']
        email= request.POST['n2']
        phone = request.POST['n3']
        experience= request.POST['n4']
        password = request.POST['n5']
        cpassword = request.POST['n6']
        if password == cpassword:
            if Register_manager.objects.filter(Email=email).exists():
                messages.info(request, "Email already Registered", extra_tags="signup")
                return redirect(registration_manager)
            else:
                val = Register_manager.objects.create(Username=name, Email=email, Phoneno=phone, Experience= experience,Password=password)
                val.save()
                messages.info(request, "Registered Successfully", extra_tags="signup")
                send_mail('Registration Successful',
                          f'{name} Your CONCERTBOOKING Account Has Been Successfully Registered. \nTHANK YOU For Registering',
                          'settings.EMAIL_HOST_USER', [email], fail_silently=False)
        else:
            messages.info(request, "Password doesn't match", extra_tags="signup")
            return redirect(registration_manager)

    return render(request, 'Registration_manager.html')

def view_user(request):
    if 'id1' in request.session:
        details= Register_user.objects.all()
        return render(request,'admin_View_user.html',{'data':details})
    return redirect(login)
def view_manager(request):
    if 'id1' in request.session:
        details= Register_manager.objects.filter(Status="pending")
        return render(request,'admin_View_manager.html',{'data':details})
    return redirect(login)


def reject_manager(request,d):
    if 'id1' in request.session:
        data=Register_manager.objects.filter(Username=d)
        data.delete()
        messages.success(request, 'Data Deleted')
        return redirect(view_manager)
    return redirect(login)


def add_event(request):
    if 'id2' in request.session:
        if request.method=='POST':
            event_name=request.POST['n1']
            location= request.POST['n2']
            date=request.POST['n3']
            time= request.POST['n4']
            gold_available_tickets=request.POST['n10']
            silver_available_tickets = request.POST['n11']
            bronze_available_tickets = request.POST['n12']
            discription = request.POST['n6']
            gold_ticket_price = request.POST['n7']
            silver_ticket_price = request.POST['n8']
            bronze_ticket_price = request.POST['n9']
            event_image = request.FILES['image']
            event_sub_image = request.FILES.getlist('subimage')
            video= request.FILES['videos']

            lis=[]
            for image in event_sub_image:
                imgs = Images(image=image)
                imgs.save()
                lis.append(imgs)
            details=Events.objects.create(Event_name= event_name,Location= location,Date=date,Time=time,Discription=discription, Event_image=event_image,Video=video, Gold_Ticket_price=  gold_ticket_price ,Silver_Ticket_price=  silver_ticket_price,  Bronze_Ticket_price=bronze_ticket_price , Gold_Available_tickets= gold_available_tickets,Silver_Available_tickets = silver_available_tickets ,Bronze_Available_tickets= bronze_available_tickets)
            details.save()
            for i in lis:
                details.Sub_images.add(i)
            messages.success(request, 'Data Saved')
            return render(request, 'manager_Add_event.html')

        return render(request, 'manager_Add_event.html')
    return redirect(login)




def view_event(request):
    if 'id2' in request.session:
        details = Events.objects.all()
        return render(request, 'manager_Viewevent.html', {'data': details})
    return redirect(login)

def view_event_admin(request):
    if 'id1' in request.session:
        details= Events.objects.filter(Status="pending")
        print(details)
        return render(request, 'admin_View_event_requests.html', {'data': details})
    return redirect(login)
def reject_event_manager(request):
    if 'id1' in request.session:
        messages.success(request, 'REJECT')
        return redirect(view_manager)
    return redirect(login)
def reject_event(request):
    if 'id1' in request.session:
        messages.success(request, 'REJECT')
        return redirect(view_event_admin)
    return redirect(login)

def delete_event(request,d):
    if 'id2' in request.session:
        data = Events.objects.filter(pk=d)
        data.delete()
        messages.success(request, 'Event deleted')
        return redirect(view_event)
    return redirect(login)




def accept_manager(request,d):
    if 'id1' in request.session:
        Register_manager.objects.filter(pk=d).update(Status="ACCEPTED")
        messages.success(request,'Accepted')
        return redirect(view_manager)
    return redirect(login)
def reject_manager(request,d):
    if 'id1' in request.session:
        Register_manager.objects.filter(pk=d).update(Status="REJECTED")
        messages.success(request,'Rejected')
        return redirect(view_manager)
    return redirect(login)

def accept_event(request,d):
    if 'id1' in request.session:
        Events.objects.filter(pk=d).update(Status="ACCEPTED")
        messages.success(request,'Accepted')
        return redirect(view_event_admin)
    return redirect(login)
def reject_event(request,d):
    if 'id1' in request.session:
        Events.objects.filter(pk=d).update(Status="REJECTED")
        messages.success(request,'Rejected')
        return redirect(view_event_admin)
    return redirect(login)

def event_accepted_by_admin(request):
    if 'id1' in request.session:
        data=Events.objects.filter(Status="ACCEPTED")
        data1 = Events.objects.filter(Status="REJECTED")
        return render(request, 'admin_Accepted_event.html', {'data': data,'data1': data1})
    return redirect(login)



def manager_accepted_by_admin(request):
    if 'id1' in request.session:
        data=Register_manager.objects.filter(Status="ACCEPTED")
        data1 = Register_manager.objects.filter(Status="REJECTED")
        return render(request, 'admin_Accepted_manager.html', {'data': data,'data1': data1})
    return redirect(login)

def concert_user(request):
    if 'id' in request.session:
        data=Events.objects.filter(Status="ACCEPTED")
        return render(request, 'User_concerts.html', {'data': data})
    return redirect(login)


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        print(email)
        try:
            user =Register_user.objects.get(Email=email)
            print(user)
        except:
            messages.info(request,"Email id not registered")
            return redirect(forgot_password)
        # Generate and save a unique token
        token = get_random_string(length=4)
        print(token)
        PasswordReset.objects.create(user=user, token=token)

        # Send email with reset link
        reset_link = f'http://127.0.0.1:8000/reset/{token}'
        try:

            send_mail('Reset Your Password', f'Click the link to reset your password: {reset_link}','settings.EMAIL_HOST_USER', [email],fail_silently=False)
            # return render(request, 'emailsent.html')

        except:
            messages.info(request,"Network connection failed")
            return redirect(forgot_password)

    return render(request, 'forgot_password.html')

def reset_password(request, token):
    # Verify token and reset the password
    print(token)
    password_reset = PasswordReset.objects.get(token=token)
    usr = Register_user.objects.get(id=password_reset.user_id)
    if request.method == 'POST':
        new_password = request.POST.get('newpassword')
        repeat_password = request.POST.get('cpassword')
        if repeat_password == new_password:
            password_reset.user.Password=new_password
            password_reset.user.save()
            # password_reset.delete()
            return redirect(login)
    return render(request, 'reset_password.html',{'token':token})


def concertview(request,d):
    if 'id' in request.session:
        data = Events.objects.get(pk=d)
        d=data.Sub_images.all()
        l=[]
        for i in d:
            l.append(i)
        print(l)
        return render(request, 'user_concert2.html', {'data': data,'h':l})
    return redirect(login)

def category(request,d):
    if 'id' in request.session:
        data = Events.objects.get(pk=d)
        # print("data=",data,"d",d)
        # d1=Booking.objects.get(ticket_details_id=d)
        return render(request, 'user_category.html', {'data': data})
    return redirect(login)


def view_event_2(request,d):
    if 'id2' in request.session:
        data = Events.objects.get(pk=d)
        d=data.Sub_images.all()
        l=[]
        for i in d:
            l.append(i)
        print(l)
        return render(request, 'manager_eventview2.html', {'data': data,'h':l})
    return redirect(login)
def admindis(request,d):
    if 'id1' in request.session:
        data = Events.objects.get(pk=d)
        d=data.Sub_images.all()
        l=[]
        for i in d:
            l.append(i)
        print(l)
        return render(request, 'admin_concertview2.html', {'data': data,'h':l})
    return redirect(login)

def demo(request,d):
    data=Events.objects.filter(pk=d)
    return render(request, 'concert_view_demo.html', {'data': data})

def demo(request,d):
    data=Events.objects.filter(pk=d)
    return render(request, 'concert_view_demo.html', {'data': data})
def about(request):
    if 'id' in request.session:
        return render(request, 'about.html')
    return redirect(login)
def amount1(request,d):
    if 'id' in request.session:
        if request.method=='POST':
            amount=request.POST['n1']
            no_tickets=request.POST['no1']
            no_tickets_gold=int(request.POST['t1'])
            no_tickets_silver=int(request.POST['t2'])
            no_tickets_browns=int(request.POST['t3'])
            data=Events.objects.get(pk=d)
            print(type(data.Silver_Available_tickets))
            print("Silver",type(no_tickets_silver))
            data.Gold_Available_tickets=data.Gold_Available_tickets-int(no_tickets_gold)
            data.Silver_Available_tickets=data.Silver_Available_tickets-no_tickets_silver
            data.Bronze_Available_tickets=data.Bronze_Available_tickets-no_tickets_browns
            data.save()
            return redirect(details, d,amount,no_tickets)
    return redirect(login)


def details(request,d,amount,no_tickets):
    if 'id' in request.session:
        f = Events.objects.get(pk=d)
        if request.method == "POST":
                s=Register_user.objects.get(Email=request.session['id'])
                user=Booking.objects.create(user_details=s,ticket_details=f,total_amount=amount,no_of_tickets=no_tickets,payment_status='PAID')
                user.save()
                return redirect('pay',amount)
        else:
            user1= Register_user.objects.get(Email=request.session['id'])
            return render(request,"Details.html",{"item":f,'user1':user1,'amount':amount,"no_tickets":no_tickets})

    return redirect(login)

def pay(request,amount):
    print(amount)
    amount = int(amount) * 100
    order_currency = 'INR'
    client = razorpay.Client(auth=("rzp_test_SROSnyInFv81S4", "WIWYANkTTLg7iGbFgEbwj4BM"))
    return render(request, "pay.html",{'amount':amount})




def success_page(request):
    if 'id' in request.session:
        usr = Register_user.objects.get(Email=request.session['id'])
        order_ids = request.session.get('order_ids', [])
        for i in order_ids:
            c = i
            b = 'PAID'
            Register_user.objects.filter(pk=c).update(payment_status=b)
        send_mail('Payment Successful',
                      f'Hey {usr.Username}, Your payment was successful and your ticket is confirmed.'
                      f'\nTHANK YOU.. \n\nBest regards,\n CONCERT BOOKING',
                  'settings.EMAIL_HOST_USER', [usr.Email], fail_silently=False)
        return render(request,"succes_page.html")
    redirect(login)

def userrecentorders(re):
    if 'id' in re.session:
        user = Register_user.objects.get(Email=re.session['id'])
        order = Booking.objects.filter(user_details=user,payment_status='PAID').order_by('-booked_date')
        print(order)
        return render(re, 'user_recent_order.html',{'data':order})
    return redirect(login)
def admin_orders(re):
    if 'id1' in re.session:
        order =Booking.objects.all()
        return render(re, 'admin_orderdetails.html',{'data':order})
    return redirect(admin_home)
def manager_orders(re):
    if 'id2' in re.session:
        order =Booking.objects.all()
        return render(re, 'managerorderdetails.html',{'data':order})
    return redirect(admin_home)

def adminorderupdate(request,d):
    if 'id1' in request.session:
        ord =Booking.objects.get(pk=d)
        print(ord)
        if request.method == 'POST':
            a = request.POST.get('odsts')
            Booking.objects.filter(pk=d).update(ticket_status=a)
            return redirect(admin_orders)
        return render(request,'admin_orderupdate.html',{'data':ord})
    return redirect(login)

from .forms import *
def update_event(request,d):
    if 'id2' in request.session:
        data = Events.objects.get(pk=d)
        if request.method=='POST':
            a = modelform(request.POST,request.FILES,instance=data)
            if a.is_valid():
                print("data", data)
                print("hello")
                a.save()
                print("hai")
                messages.success(request,"updated successfully")
                return redirect(view_event)
        a=modelform(instance=data)
        return render(request,'Update_event.html',{'key':a})
    return redirect(login)











