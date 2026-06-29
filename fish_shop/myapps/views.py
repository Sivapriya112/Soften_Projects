from django.shortcuts import render,redirect
from .models import*
from django.http import HttpResponse
from django.contrib import messages
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
import razorpay
from .forms import *
# Create your views here.
def about(a):
    return render(a,'about.html')
def bloggrid(a):
    return render(a,'bloggrid.html')
def booking(a):
    return render(a,'booking.html')
def contact(a):
    return render(a,'contact.html')
def index(a):
    return render(a,'index.html')
def price(a):
    return render(a,'price.html')
def service(a):
    return render(a,'service.html')
def blogdetail(a):
    return render(a,'blogdet.html')
def reg(re):
    if re.method =='POST':
        n=re.POST['name']
        h=re.POST['phone']
        e=re.POST['email']
        p=re.POST['password']
        c=re.POST['cpass']
        if p==c:
            if register.objects.filter(email=e).exists():
                messages.info(re, "Email already Registered", extra_tags="signup")
                return redirect(reg)
            else:
                val=register.objects.create(username=n,email=e,phone=h,password=p)
                val.save()
                messages.info(re,"User Registered Successfully", extra_tags="signup")
                return redirect(login)
        else:
            messages.info(re, "Password doesn't match", extra_tags="signup")
            return redirect(reg)

    return render(re,'register.html')
def login(a):
    if a.method=='POST':
        n=a.POST['name']
        p=a.POST['pass']
        try:
           data=register.objects.get(username=n)
           if data.password==p:
             a.session['user']=n
             return redirect(userhome)

           else:
              messages.error(a,'Invalid password')
        except Exception:
            if n =='admin' and p=='4321':
                a.session['admin']=n
                return redirect(adminhome)
            else:
                messages.success(a,'Invalid username')
    return render(a,'login.html')
def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        print(email)
        try:
            user =register.objects.get(email=email)
            print("User",user)
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
    # usr = register.objects.get(id=password_reset.user_id)
    if request.method == 'POST':
        new_password = request.POST.get('newpassword')
        repeat_password = request.POST.get('cpassword')
        if repeat_password == new_password:
            password_reset.user.password=new_password
            password_reset.user.save()
            # password_reset.delete()
            return redirect(login)
    return render(request, 'reset_password.html',{'token':token})

def logout(r):
   r.session.flush()
   return redirect(login)
# -------------------userhome-----------------------------------
def userhome(a):
    if 'user' in a.session:
        user=register.objects.get(username=a.session['user'])
        y=a.session['user']
        detail=fish.objects.all()
        l=[]
        l1=[]
        try:
            data1=cart.objects.filter(user_details=user)
            for i in data1:
                l.append(i.product_details)
        except:
            pass
        try:
            wish=wishlist.objects.filter(user_details=user)
            for i in wish:
                l1.append(i.product_details)
        except:
            pass
    return render(a,'userhome.html',{'data':detail,'y':y,'data_1':data1,'wish_1':wish,'list':l,'list1':l1})
    return redirect()
def categories(a):
    return render(a,'categories.html')
def community(a):
    data1=fish.objects.filter(category='COMMUNITY FISH')
    return render(a,'community.html',{'data':data1})
def aggressive(a):
    data=fish.objects.filter(category='AGGRESSIVE FISH')
    return render(a,'aggressive.html',{'data':data})
def goldfish(a):
    data=fish.objects.filter(category='GOLD FISH')
    return render(a,'goldfish.html',{'data':data})
def fighter(a):
    data=fish.objects.filter(category='FIGHTER')
    return render(a,'fighter.html',{'data':data})
def koicarp(a):
    data=fish.objects.filter(category='KOI CARP')
    return render(a,'koicarp.html',{'data':data})
def add_cart(a,k):
    if 'user' in a.session:
       data=fish.objects.get(pk=k)
       user=register.objects.get(username=a.session['user'])
       cartdet=cart.objects.create(user_details=user,product_details=data)
       cartdet.save()
       messages.success(a,'add to cart successfully')
       return redirect(userhome)
def display_cart(a):
    if 'user' in a.session:
        d=register.objects.get(username=a.session['user'])
        data=cart.objects.filter(user_details=d)
        print(data)
        qty=1
        total=0
        c=1
        for i in data:
           print(i.product_details.fprice)
           c=c+1
           total +=i.product_details.fprice*i.quantity
           print(total)
        # return render(request,'cart.html',{'key':user,'tota':total})
        return render(a,'cart.html',{'data':data,'total1':total})
def checkoutcart(re,total):
    user = register.objects.get(username=re.session['user'])
    print(user,"User")
    pro=cart.objects.filter(user_details=user)
    print(pro)
    order_ids = []
    if re.method == 'POST':
        a = re.POST.get('user_name')
        c = re.POST.get('user_address')
        d = re.POST.get('user_city')
        e = re.POST.get('user_state')
        g = re.POST.get('user_zipcode')
        h = re.POST.get('user_phone')
        l = int(re.POST.get('user_total'))
        for i in pro:
            cn = i.product_details
            cq = i.quantity
            ct = i.product_details.fprice * i.quantity
            v=deliverydetails(userdetails=user, fullname=a,address=c,city=d,state=e,pincode=g,productdetails=cn,quantity=cq,total_price=ct,)
            v.save()
            de=cart.objects.filter(product_details=cn)
            de.delete()
            value1 = v.pk
            order_ids.append(value1)
            fish.objects.filter(pk=i.product_details.pk).update(fstock=i.product_details.fstock-cq)
        re.session['order_ids'] = order_ids
        return redirect(pay_cart,l)
    return render(re,'checkoutcart.html',{'user':user,'data':pro,'total':total})
def pay_cart(request,amount):
    print(amount)
    amount = int(amount) * 100
    order_currency = 'INR'
    client = razorpay.Client(auth=("rzp_test_SROSnyInFv81S4", "WIWYANkTTLg7iGbFgEbwj4BM"))
    return render(request, "payment.html", {'amount': amount})
def cart_delete(re,d):
    data=cart.objects.get(pk=d)
    data.delete()
    messages.success(re,'remove from cart')
    return redirect(display_cart)
def increment(re,cart_id):
    data=cart.objects.get(pk=cart_id)
    if data.product_details.fstock > 1:
        data.quantity+= 1
        data.save()
        data.fprice= data.quantity * data.product_details.fprice
        data.save()
    return redirect(display_cart)
def decrement_quantity(request, cart_id):
    data = cart.objects.get(pk=cart_id)
    if data.quantity> 1:
        data.quantity -= 1
        data.save()
    return redirect(display_cart)
def Wishlist(request,pid):
       if 'user' in request.session:
           user=register.objects.get(username=request.session['user'])
           product=fish.objects.get(pk=pid)
           if wishlist.objects.filter(product_details_id=pid).exists():
               messages.error(request,'Already Added in wishlist')
           else:
               cartdetails=wishlist.objects.create(user_details=user,product_details=product)
               cartdetails.save()
               messages.success(request,'added to wishlist')
           return redirect(userhome)
       return render(request,'userhome.html')
def display_wishlist(a):
    user_name=register.objects.get(username=a.session['user'])
    userdetails=wishlist.objects.filter(user_details=user_name)
    return render(a,'wishlist.html',{'key':userdetails})
def remove_wishlist(request,d):
    data=wishlist.objects.filter(pk=d)
    data.delete()
    messages.success(request,'removed from wishlist')
    return redirect(display_wishlist)
#track order #
def userrecentorders(re):
    if 'user' in re.session:
        user = register.objects.get(username=re.session['user'])
        order = deliverydetails.objects.filter(userdetails=user,payment_status ='PAID').order_by('-purchase_date')
        print(order)
        return render(re, 'recentorder.html',{'data':order})
    return redirect(login)
#shipping details#
def details(request,d):
    f = fish.objects.get(pk=d)
    if request.method == "POST":
        s=register.objects.get(username=request.session['user'])
        amount=f.fprice
        City=request.POST.get('city')
        Address= request.POST.get('address')
        State=request.POST.get('state')
        Pincode=request.POST.get('pincode')
        user=deliverydetails.objects.create(pincode=Pincode,city=City,address=Address,state=State,userdetails=s,productdetails=f,total_price=amount,payment_status='PAID',)
        user.save()
        f.fstock=f.fstock-1
        f.save()
        messages.success(request, 'payment succuessfull')
        return redirect('pay',amount)

    else:
        user1= register.objects.get(username=request.session['user'])
        return render(request,"orderdetails.html",{"user1":user1,"item":f})
def pay(request,amount):
    print(amount)
    amount = int(amount) * 100
    order_currency = 'INR'
    client = razorpay.Client(auth=("rzp_test_SROSnyInFv81S4", "WIWYANkTTLg7iGbFgEbwj4BM"))
    return render(request, "payment.html", {'amount': amount})
def success(request):
    return render(request,'success.html')
def Log_out(a):
    a.session.flush()
    return redirect(login)
def profile(re):
    if 'user' in re.session:
        data = register.objects.get(username=re.session['user'])
        return render(re,'userprofile.html',{'data':data})
    return redirect(login)
def updateprofile(re):
    if 'user' in re.session:
        if re.method == 'POST':
            b = re.POST['phoneno']
            c = re.POST['email']
            d = re.POST['username']
            register.objects.filter(username=re.session['user']).update(  phone=b, email=c, username=d)
            messages.success(re,'Profile Updated')
        return redirect(profile)
def changepassword(request):
    if 'user' in request.session:
        if request.method == 'POST':
            a = request.POST.get('current_password')
            b = request.POST.get('new_password')
            c = request.POST.get('confirm_password')
            try:
                data = register.objects.get(username=request.session['user'])
                if data.password == a:
                    if b == c:
                        register.objects.filter(username=request.session['user']).update(password=b)
                        messages.success(request, 'Password Updated')
                        return redirect(profile)
                    else:
                        messages.error(request, 'Passwords Do not Match')
                        return redirect(profile)
                else:
                    messages.error(request, 'Password Incorrect')
                    return redirect(profile)
            except Exception:
                return redirect(profile)
def fish_details(request,d):
    data = fish.objects.filter(pk=d)
    return render(request,'description.html',{'data':data})
# ------------------------adminhome---------------------------------------
def adminhome(a):
    return render(a,'adminhome.html')
def viewuser(a):
    cn=register.objects.all()
    return render(a,'viewuser.html',{'data':cn})
def add_product(t):
    if t.method=='POST':
      n=t.POST['name']
      p=t.POST['price']
      s=t.POST['stock']
      i=t.FILES['image']
      d=t.POST['des']
      c=t.POST['category']
      details=fish.objects.create(fishname=n,fprice=p,fstock=s,fimage=i,description=d,category=c)
      details.save()
      return render(t,'addproduct.html')
    return render(t,'addproduct.html')
def display_product(a):
    detail=fish.objects.all()
    return render(a,'display.html',{'data':detail})
def low_stock(re):
    # if 'admin' in re.session:
        a = fish.objects.all()

        l=[]
        for i in a:
            if i.fstock < 5:
                l.append(i)
                # print(i.Stock)
        print("l",l)
        return render(re,'lowstock.html',{'item':l})
def admin_edit(request,d):

        dt = fish.objects.get(pk=d)

        if request.method == 'POST':
            e = edit_image(request.POST, request.FILES,instance=dt)
            if e.is_valid():
                e.save()
                messages.success(request, 'updated successfully')
                return redirect(display_product)
        e=edit_image(instance=dt)
        return render(request, 'adminedit.html', {'data': e})
def admin_delete(o,k):
    data = fish.objects.get(pk=k)
    data.delete()
    messages.success(o,'delete')
    return redirect(display_product)
def admin_orders(re):
    if 'admin' in re.session:
        order = deliverydetails.objects.all()
        print("Order",order)
        return render(re, 'adminorderdetails.html',{'data':order})
    return redirect(login)
    # return redirect(adminhome)
def adminorderupdate(request,d):
    if 'admin' in request.session:
        ord = deliverydetails.objects.get(pk=d)
        print(ord)
        if request.method == 'POST':
            a = request.POST.get('odsts')
            b = request.POST.get('inst')
            deliverydetails.objects.filter(pk=d).update(product_status=a, instruction=b)
            return redirect(admin_orders)
        return render(request,'adminorderupdate.html',{'data':ord})
    return redirect(login)
def search(p):
    if p.method=='POST':
        s=p.POST['search']
        data3=register.objects.filter(username=s)
        return render(p,'register.html',{'date':data3})
    return render(p,'register.html')
def logout(a):
    a.session.flush()
    return redirect(login)
