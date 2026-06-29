import datetime

from django.http import HttpResponse
from django.shortcuts import render,redirect
from requests import session

from .models import *
from django.contrib import messages
import razorpay
from.bform import *
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.
def index(request):
    data = addadopt.objects.all()
    return render(request, 'index.html', {'r': data})
def about(request):
    return render(request,'about.html')
def blog(request):
    return render(request,'blog.html')
def contact(request):
    return render(request,'contact.html')
def detail(request):
    return render(request,'detail.html')
def adoption(request):
    data = addadopt.objects.all()
    return render(request, 'adoption.html', {'r': data})
def product(request):
    data=addproduct.objects.all()
    return render(request,'product.html',{'r':data})
def service(request):
    return render(request,'service.html')
def team(request):
    return render(request,'team.html')
def testimonial(request):
    return render(request,'testimonial.html')
def edit(request):
    return render(request,'edit.html')
def userreg(request):
    return render(request,'editreg.html')
def userprofile(request):
        if request.method == 'GET':
            a = request.session['uid']
            data = login.objects.filter(username=a)
            return render(request, 'profile.html', {'r': data})
        else:
            return render(request, 'userindex.html')

def update_profile(request):
    if request.method == 'GET':
        a = request.session['uid']
        data = login.objects.filter(username=a)
        # return render(request, 'profile.html', {'r': data})
        return render(request, 'update_prof.html', {'r': data})

def serviceapp(request):
    return render(request,'serviceapp.html')
def signup(request):
    if request.method=='POST':
        a = request.POST['n1']
        b = request.POST['n2']
        c = request.POST['n3']
        d = request.POST['n4']
        e = request.POST['n5']
        f = request.POST['n6']
        z = user.objects.filter(username=d)
        t = login.objects.filter(email=c)
        if list(z) == []:
            if list(t) == []:
                data = login.objects.create(name=a, mob=b, email=c, username=d, address=f)
                data.save()
                data1 = user.objects.create(username=d, password=e)
                data1.save()
                return render(request, 'index.html')
            else:
                messages.info(request, 'email already exists..')
                return render(request, 'editreg.html')
                # url = 'signup.html'
                # msg = '''<script>alert('email already exist')
                #                     window.location='%s'</script>''' % (url)
                # return HttpResponse(msg)
                # return redirect(signup)
        else:
            messages.info(request, 'username already exists')
            return render(request, 'editreg.html')
            # url = 'signup.html'
            # msg = '''<script>alert('username already exist')
            #         window.location='%s'</script>''' % (url)
            # return HttpResponse(msg)
            # return redirect(signup)
    else:
        return render(request, 'editreg.html')


def profile1(request):
    if 'uid' in request.session:
        d = request.session ['uid']
        u = login.objects.get(username=d)
        return render(request,'userindex.html',{'r':u})
    elif 'aid' in request.session:
        d = request.session['aid']
        return render(request,'adindex.html')
    else:
        return render(request, 'index.html')

def log(request):
    if request.method == 'POST':
        d = request.POST['n4']
        e = request.POST['n5']
        if d == 'admin' and e == 'admin':
            request.session['aid'] = d #admin session created
            return redirect(profile1)
            # return render(request,'adindex.html')
        else:
           try:
               data = user.objects.get(username=d)
               if data.password == e:
                   request.session['uid'] = d #user session created
                   return redirect(profile1)

               else:
                   messages.info(request,'login failed,password incorrect..')
                   return render(request,'edit.html')
           except Exception as k:
               return HttpResponse(k)

def logout(request):
    if 'uid' in request.session:
        request.session.flush()
        return redirect(index)
    elif 'aid' in request.session:
        request.session.flush()
        return redirect(index)
    else:
        request.session.flush()
        return redirect(index)
def change(request):
    return render(request,'chngepwd.html')
def chngepwd(request):
    if request.method == 'POST':
        d = request.POST['n4']
        e = request.POST['n5']
        f = request.POST['n6']
        data = user.objects.filter(username=d,password=e)
        data.update(password=f)
        return render(request,'edit.html')

#user
def userindex(request):
    data = addadopt.objects.all()
    return render(request, 'userindex.html', {'data': data})
def userabout(request):
    return render(request,'userabout.html')
def userservice(request):
    return render(request,'userservice.html')
def userproduct(request):
    data=addproduct.objects.all()
    return render(request,'userproduct.html',{'r':data})
# def useradoption(request):
#     return render(request,'useradoption.html')
def adopt(request):
    if request.method == 'GET':
        a = request.session['uid']
        data = login.objects.filter(username=a)
        # return render(request, 'profile.html', {'r': data})
        return render(request,'adopt.html',{'r': data})
def serviceapp(request):
    if request.method == 'GET':
        a = request.session['uid']
        data = login.objects.filter(username=a)
        # return render(request, 'profile.html', {'r': data})
        return render(request,'serviceapp.html',{'r': data})
def userteam(request):
    return render(request,'userteam.html')
def usertestimonial(request):
    return render(request,'usertestimonial.html')
def userblog(request):
    return render(request,'userblog.html')
def userdetail(request):
    return render(request,'userdetail.html')
def serviceappoinment(request):
    if request.method == 'POST':
        a = request.POST['s1']
        b = request.POST['s2']
        c = int(request.POST['s3'])
        d = request.POST['s4']
        e = request.POST['s5']
        f = request.POST['s6']
        g = request.POST['s7']
        data = appoinment.objects.create(name=a, email=b, mob=c, pet=d, service=e, date=f, time=g,status='pending')
        data.save()
        return redirect(serviceapp)

def userserviceview(request):
    if request.method == 'GET':
        a = request.session['uid']
        data = appoinment.objects.filter(name=a)
        return render(request, 'userserviceview.html', {'r': data})
    else:
        return render(request, 'userindex.html')

def adopt_req(request):
    if request.method == 'POST':
        a = request.POST['a1']
        b = request.POST['a2']
        c = request.POST['a3']
        d = request.POST['a4']
        e = request.POST['a5']
        data = adopt_table.objects.create(username=a, fullname=b, email=c ,mob=d, message=e, status='pending')
        data.save()
        return redirect(adopt)

def useradoptview(request):
    if request.method == 'GET':
        a = request.session['uid']
        data = adopt_table.objects.filter(username=a)
        return render(request,'useradoptview.html',{'r': data})
    else:
        return render(request,'userindex.html')



#admin
def adindex(request):
    data = addadopt.objects.all()
    return render(request, 'adindex.html', {'r': data})
def adabout(request):
    return render(request,'adabout.html')
def adproduct(request):
    return render(request,'adproduct.html')
def adadoption(request):
    return render(request,'adadoption.html')
def adserviceview(request):
    if request.method == 'GET':
        data = appoinment.objects.filter(status='confirmed')
        print(data)
        return render(request, 'adserviceview.html',{'r': data})

def disp_appoinment(request):
    if request.method == 'GET':
        data = appoinment.objects.all()
        return render(request,'adservice.html',{'r': data})
def disp_req(request):
    if request.method == 'GET':
        data = adopt_table.objects.all()
        return render(request,'adrequest.html',{'r': data})
# admin-reject adopt req
def adopt_update(request):
    if request.method == 'POST':
        a = request.POST['b1']
        # b = request.POST['b2']
        d = adopt_table.objects.filter(username=a)
        d.update(status='approved')
        return redirect(disp_req)
    else:
        return render(request,'adindex.html')

# admin-reject adopt req
def adopt_delete(request):
    if request.method == 'POST':
        a = request.POST['b1']
        # b = request.POST['b2']
        d = adopt_table.objects.filter(username=a,)
        d.delete()
        return redirect(disp_req)
    else:
        return render(request, 'adindex.html')

# admin- approve service appoinment
def accept(request):
    if request.method=='POST':
        a = request.POST['b1']
        b = request.POST['b2']
        c = int(request.POST['b3'])
        l = appoinment.objects.filter(name=a, email=b, mob=c)
        l.update(status='confirmed')
        # send_mail('Confirm Appointment', 'your appointment is confirmed',
        #           'settings.EMAIL_HOST_USER', [c], fail_silently=False)
        return redirect(disp_appoinment)
    else:
        return render(request,'adindex.html')

# admin-reject service appointment
def reject(request):
        if request.method == 'POST':
            a = request.POST['b1']
            b = request.POST['b3']
            d = appoinment.objects.filter(name=a, mob=b)
            d.update(status='Rejected')
            return redirect(disp_appoinment)
        else:
            return render(request, 'bookreq.html')



def new(request):
    return render(request,'newproduct.html')
# def update_prof(request):
#     return render(request,'update_prof.html')



def up_prof(request):
    if request.method == 'POST':
        b = request.POST['b1']
        c = request.POST['b2']
        d = request.POST['b3']
        e = request.POST['b4']
        f = request.POST['b5']
        u = login.objects.filter(username=e)
        u.update(name=b,mob=c,email=d,address=f)
        return redirect(userprofile)
    else:
        return render(request, 'userindex.html')

def add_product(request):
        return render(request,'add_product.html')

def add(request):
        if  request.method == 'POST':
            a=  request.POST['n1']
            b = request.POST['n2']
            c = request.POST['n3']
            e =  request.FILES['n4']
            data = addproduct.objects.create(productname=a,price=b,quantity=c,image=e)
            data.save()
            messages.success(request,'Product Added')
            return render(request,'add_product.html')

def adproductview(request):
        if request.method == 'GET':
            data = addproduct.objects.all()
            return render(request, 'adproduct.html', {'r': data})
        else:
            return render(request, 'userindex.html')

def adviewproduct(request):
    data=addproduct.objects.all()
    return render(request, 'adindex.html', {'r': data})
def usercart(request):
    return render(request,'cart.html')


def cartview (request):
    u = login.objects.get(username=request.session['uid'])
    data=cart.objects.filter(user_details=u)
    total=0
    quantity=0

    for i in data:
        i.total_price=i.product_details.price
        i.total_price=i.product_details.price * i.quantity
        print(i.total_price)
        total+=i.total_price
        quantity+=1
    return render(request,'cart.html',{'r':data,'total':total,'quantity':quantity})

def add_cart(request, i, userviewproduct=None):
    a = addproduct.objects.get(pk=i)
    u = login.objects.get(username=request.session['uid'])
    if cart.objects.filter(product_details=a).exists():
       data = cart.objects.get(product_details=a)
       data.quantity+=1
       data.save()
    else:
        cart.objects.create(product_details=a, user_details=u,total_price=a.price).save()
    return redirect(userproduct)

# from wishlist to cart
def add_cart1(request, i):
    a = addproduct.objects.get(pk=i)
    u = login.objects.get(username=request.session['uid'])
    if cart.objects.filter(product_details=a).exists():
        data = cart.objects.get(product_details=a)
        data.quantity += 1
        data.save()
    else:
        cart.objects.create(product_details=a, user_details=u, total_price=a.price).save()
    return redirect(userproduct)


def quantity(request,i):
    data =cart.objects.get(pk=i)
    data.quantity +=1
    data.total_price=data.quantity*data.product_details.price
    data.save()
    return redirect(cartview)
def quan_tity(request,i):
    data = cart.objects.get(pk=i)
    data.quantity -=1
    if data.quantity <1:
        data.delete()
    else:
     data.save()
    return redirect(cartview)
def userwishlist(request):
    u = login.objects.get(username=request.session['uid'])
    data = wishlist.objects.filter(user_details=u)
    return render(request, 'wishlist.html', {'r': data})

def add_wishlist(request,i):
    a = addproduct.objects.get(pk=i)
    u = login.objects.get(username=request.session['uid'])
    wishlist.objects.create(product_details=a, user_details=u).save()
    return redirect(userproduct)

def trash(request,i):
    data=cart.objects.get(pk=i)
    data.delete()
    return redirect(cartview)

def remove(request,i):
    data = wishlist.objects.get(pk=i)
    data.delete()
    return redirect(userwishlist)

def paymentform(request):
    if request.method == 'GET':
        u = login.objects.get(username=request.session['uid'])
        data = cart.objects.filter(user_details=u)
        return render(request, 'paymentform.html', {'r': data})
    else:
        return render(request, 'userindex.html')

def pay(request, id):
    amount = (id) * 100
    request.session['amount'] = id
    order_currency = 'INR'
    client = razorpay.Client(
        auth=("rzp_test_SROSnyInFv81S4", "WIWYANkTTLg7iGbFgEbwj4BM"))
    # cursor = connection.cursor()
    # cursor.execute(
    #     "update inspection_details set status='completed', fine_paid_date = curdate() where insp_id='" + str(
    #         id) + "' ")

    # payment = client.order.create({'amount': amount, 'currency': 'INR', 'payment_capture': '1'})
    return render(request, "pay.html", {'r': amount})

def success(request):
     if 'uid' in request.session:
        print(request.session['amount'])
        u = login.objects.get(username=request.session['uid'])
        data = cart.objects.filter(user_details=u)
        date=datetime.datetime.now()
        for i in data:
            myorder.objects.create(user_details=u,product_details=i.product_details,product_status='Order confirmed', quantity=i.quantity, payment_amount=(request.session['amount']),order_date=date ).save()
            data.delete()
            return render(request, 'success.html',{'r': data})
        else:
            return redirect(userindex)

def my_order(request):
    if 'uid' in request.session:
        u = login.objects.get(username=request.session['uid'])
        data = myorder.objects.filter(user_details=u)

        return render(request, 'myorder.html', {'r': data})

    else:
        return redirect(userindex)

def orders(request):
    data = myorder.objects.all()
    return render(request, 'order.html', {'r': data})

def order_update(request,i):
    data = myorder.objects.get(pk=i)
    if request.method == 'POST':
        a = request.POST['status']
        data.product_status = a
        data.save()
        # messages.success(request, 'order updated')
        return redirect(orders)
    else:
        return redirect(orders)


def add_adopt(request):
    if request.method == 'POST':
        a = request.FILES['n1']
        b = request.POST['n2']
        c = request.POST['n3']
        d = request.POST['n4']
        data = addadopt.objects.create(image=a, breed=b, age=c, behaviour=d)
        data.save()
        messages.success(request, 'Added')
        return redirect(adadoption)

def useradoption(request):
    if request.method == 'GET':
        data = addadopt.objects.all()
        return render(request, 'useradoption.html', {'r': data})
    else:
        return render(request, 'userindex.html')

# def indexadoption(request):
#     data = addadopt.objects.all()
#     return render(request, 'adoption.html', {'r': data})



def manage(request):
    if 'aid' in request.session:
        data = addproduct.objects.all()
        return render(request,"manage.html",{'r':data})
    else:
        return redirect(adindex)


def product_update(request,i):
    if 'aid' in request.session:
        data = addproduct.objects.get(pk=i)
        f = modelform(instance = data)
        if request.method == 'POST':
             f = modelform(request.POST, request.FILES, instance = data)
             if f.is_valid():
                 f.save()
                 messages.success(request,'Updated successfully')
                 return redirect(manage)
             return redirect(manage)
        return render(request, 'product_update.html', {'data': data,'f':f})
    else:
        return redirect(adindex)

def delete(request,i):
    if 'aid' in request.session:
        data=addproduct.objects.get(pk=i)
        data.delete()
        messages.error(request,'Product Removed')
        return redirect(manage)
    else:
        return redirect(adindex)

def contactform(request):
    if request.method == 'POST':
        a = request.POST['c1']
        b = request.POST['c2']
        c = request.POST['c3']
        d = int(request.POST['c4'])
        e = request.POST['c5']
        data = contact_table.objects.create(username=a, name=b, email=c, mob=d, message=e)
        data.save()
        return render(request, 'contact.html')

def complaint(request):
    if request.method == 'GET':
        data = contact_table.objects.all()
        return render(request,'complaint.html',{'r': data})

def productup(request):
    return render(request,'product_update.html')



def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            u = login.objects.get(email=email)
        except Exception:
            messages.info(request,"Email id not registered")
            return render(request, 'forgot.html')
        # Generate and save a unique token
        token = get_random_string(length=32)
        PasswordReset.objects.create(user=u, token=token)

        # Send email with reset link
        reset_link = f'http://127.0.0.1:2000/reset/{token}'
        try:
            send_mail('Reset Your Password', f'Click the link to reset your password: {reset_link}','settings.EMAIL_HOST_USER', [email],fail_silently=False)
            # return render(request, 'emailsent.html')
        except:
            messages.info(request,"Network connection failed")
            return redirect(forgot_password)

    return render(request, 'forgot.html')


def reset_password(request, token):
    print("jsdgfkhdgfkjdgfkdj")
    # Verify token and reset the password
    password_reset = PasswordReset.objects.get(token=token)
    print(password_reset)
    # usr = user.objects.get(id=password_reset.user_id)
    if request.method == 'POST':
        new_password = request.POST.get('newpassword')
        repeat_password = request.POST.get('cpassword')
        if repeat_password == new_password:
            u = password_reset.user.username
            user.objects.filter(username=u).update(password=new_password)

            # password_reset.user.password=new_password
            # password_reset.user.save()
            # # password_reset.delete()
            return redirect(edit)
    return render(request, 'reset.html',{'token':token})