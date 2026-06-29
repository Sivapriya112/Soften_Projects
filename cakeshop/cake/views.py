from django.shortcuts import render, redirect

# Create your views here.
from django.http import HttpResponse
from .models import *
from .forms import *
from django.contrib import messages




def about(request):
    return render(request, 'about.html')


def index(request):
    return render(request, 'index.html')


def contact(request):
    return render(request, 'contact.html')


def menu(request):
    return render(request, 'menu.html')


def service(request):
    return render(request, 'service.html')


def testimonial(request):
    return render(request, 'testimonial.html')


def team(request):
    return render(request, 'team.html')


def login(a):
    if a.method == 'POST':
        n = a.POST['email']
        p = a.POST['password']
        try:
            data = register.objects.get(email=n)
            if data.password == p:
                a.session['user'] = n
                return redirect(userhome)

            else:
                messages.error(a, 'Invalid password')
        except Exception:
            if n == 'admin@gmail.com' and p == '4321':
                a.session['admin'] = n
                return redirect(adminhome)
            else:
                messages.error(a, 'Invalid username')
                return render(a, 'login.html', {'n': n, 'p': p})
    return render(a, 'login.html')


# def login(request):
#     if request.method == 'POST':
#         email = request.POST['email']
#         password = request.POST['password']
#
#         try:
#             # Attempt to get the user with the provided email
#             user = register.objects.get(email=email)
#
#             # Check if the password matches
#             if user.password == password:
#                 if user.role == 'user':
#                     request.session['user'] = email
#                     return redirect('userhome')
#                 elif user.role == 'deliveryboy':
#                     request.session['deliveryboy'] = email
#                     return redirect('deliveryhome')
#                 else:
#                     messages.error(request, 'Invalid user role')
#             else:
#                 messages.error(request, 'Invalid password')
#
#         except register.DoesNotExist:
#             # Check if the admin credentials are correct
#             if email == 'admin@gmail.com' and password == '4321':
#                 request.session['admin'] = email
#                 return redirect('login')
#             else:
#                 messages.error(request, 'Invalid username')
#
#         except Exception as e:
#             # Log the exception (e.g., using logging library)
#             messages.error(request, 'An unexpected error occurred')
#
#         # If login fails, render the login page with the provided credentials
#         return render(request, 'login.html', {'email': email, 'password': password})
#
#     # Render the login page for GET requests
#     return render(request, 'login.html')


def admin_login(r):
    if r.method=="POST":
        a=r.POST['n1']
        b=r.POST["n2"]
    #     try:
    #         data=register.objects.get(email=a)
    #         print(data.password)
    #         if data.password==b:
    #             r.session['user']=a
    #             print("logged")
    #             return redirect(userhome)
    #         else:
    #             messages.error(r,'incorrect username or password')
    #     except Exception:
    #         if a=='admin@gmail.com' and b=='12345':
    #             return redirect(admin)
    # return render(r,'login.html')
        if a=='admin@gmail.com' and b=='4321':
            r.session['admin']=a
            return redirect(adminhome)
        else:
            messages.error(r,'only registered user can login')
        return render(r,'admin_login.html')
    return render(r,'admin_login.html')


def user_login(re):
    if re.method=="POST":
        a=re.POST['n1']
        b=re.POST['n2']
        try:
            data1=register.objects.get(email=a)
            if data1.password==b :
            # messages.success(re,"You can login")
                re.session['user']=a
                return redirect(userhome)
            else:
                messages.error(re,"incorrect login password")
        except Exception:
            messages.error(re,'invalid account')

    return render(re,'user_login.html')



def dboy_login(r):
    if r.method=='POST':
        a=r.POST['n1']
        b=r.POST['n2']
        try:

            data=dboy.objects.get(email=a)
            print(data)

            if data.password==b:
                print("hai")
                if data.status=='accepted':
                    print("hello")
                    r.session['boy']=a
                    return redirect(deliveryhome)
                else:
                    messages.error(r,'admin has not approved your registration')
        except:
            messages.error(r,'only registered user can login')
            return render(r,'delivery_login.html')
    return render(r, 'delivery_login.html')



# def registerr(re):
#     if re.method == 'POST':
#         a = re.POST['username']
#         b = re.POST['phone']
#         c = re.POST['email']
#         d = re.POST['password']
#         e = re.POST['cpass']
#         if d == e:
#             data = register.objects.create(username=a, phone=b, email=c, password=d)
#             data.save()
#             messages.success(re, "Registered Successfully")
#             return redirect(login)
#         else:
#             messages.error(re, "Password incorrect")
#     return render(re, 'register.html')



def registerr(request):
    if request.method == "POST":
        a = request.POST['username']
        b = request.POST['phone']
        c = request.POST['email']
        d = request.POST['password']
        e = request.POST['cpass']
        if register.objects.filter(email=c) and  register.objects.filter(phone=b).exists():
            messages.error(request,'user already exist')
            return redirect(registerr)
        elif d == e:
            data = register.objects.create(email=c, username=a, password=d,phone=b)
            data.save()
            messages.success(request, 'registration succesfully')
        else:
            messages.error(request, 'password mismatches')

    # return render(request, 'register.html')
    return render(request,'register.html')




# import re
# from django.core.validators import validate_email
# from django.core.exceptions import ValidationError
#
#
# def registerr(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         phone = request.POST['phone']
#         email = request.POST['email']
#         password = request.POST['password']
#         confirm_password = request.POST['cpass']
#
#         # Validation checks
#         errors = []
#
#         if not username:
#             errors.append("Username is required.")
#
#         if not phone or not re.match(r'^\+?1?\d{9,15}$', phone):
#             errors.append("Enter a valid phone number.")
#
#         try:
#             validate_email(email)
#         except ValidationError:
#             errors.append("Enter a valid email address.")
#
#         if len(password) < 8:
#             errors.append("Password must be at least 8 characters long.")
#
#         if password != confirm_password:
#             errors.append("Passwords do not match.")
#
#         if errors:
#             for error in errors:
#                 messages.error(request, error)
#             return render(request, 'register.html')
#             data = register.objects.create(username=username, phone=phone, email=email, password=password)
#             data.save()
#             messages.success(request, "Registered Successfully")
#         return redirect(user_login)
#
#     return render(request, 'register.html')


def dboy_reg(r):
    if r.method=='POST':
        a = r.POST['n1']
        b = r.POST['n2']
        c = r.POST['n3']
        d = r.POST['n4']
        e = r.POST['n5']
        f = r.POST['n6']
        g = r.POST['n7']
        if f==g:
            data=dboy.objects.create(name=a,email=b,phno=c,d_license=d,username=e,password=f)
            data.save()
            messages.success(r, 'registered successfully')
        else:
            messages.error(r, 'password mismatch')
    return render(r,'dboy_reg.html')

def employee_details(r):
    data=dboy.objects.all()
    return render(r,'employee_details.html',{'data':data})

def accept(r,d):
    dboy.objects.filter(pk=d).update(status='accepted')
    messages.success(r,'delivery associate accepted')
    return redirect(employee_details)

def reject(r,d):
    dboy.objects.filter(pk=d).update(status='rejected')
    messages.success(r, 'delivery associate rejected')
    return redirect(employee_details)

def log(request):
    return render(request, 'log.html')



def adminhome(re):
    return render(re, 'adminhome.html')

def deliveryhome(re):
    return render(re, 'deliveryhome.html')

def addproduct(request):
    if request.method == "POST":
        a = request.POST['n1']
        b = request.POST['n2']
        c = request.POST['n3']
        d = request.POST['n4']
        e = request.POST['n5']
        f = request.FILES['n6']
        data = Add_Product.objects.create(ProductName=a, Price=b, Quantity=c, Models=d, Category=e, image=f)
        data.save()
        messages.success(request, ' Added')
    return render(request, 'addproduct.html')


def userhome(request):
    data = Add_Product.objects.all()
    return render(request, 'userhome.html', {'data': data})


def addcart(request, d):
    if 'user' in request.session:
        data = Add_Product.objects.get(pk=d)
        user = register.objects.get(email=request.session['user'])
        if cart.objects.filter(product_details_id=d).exists():
            d1 = cart.objects.get(product_details_id=d)
            d1.quantity += 1
            d1.save()
            return redirect(mycart)

        else:
            cart.objects.create(product_details=data, user_details=user,total_price=data.Price).save()
            messages.success(request, 'added to cart')
            return redirect(mycart)
    return redirect(user_login)


def mycart(re):
    if 'user' in re.session:
        user = register.objects.get(email=re.session['user'])
        data = cart.objects.filter(user_details=user)
        total_price = 0
        quantity_count = data.count()
        for i in data:
            a = i.product_details.Price
            b = i.quantity
            c = a * b
            total_price += c
        return render(re, 'mycart.html',{'data': data, 'quantity_count': quantity_count, 'total_price': total_price})
    return redirect(mycart)

    return render(re, 'mycart.html')


def addwhishlist(request, d):
    if 'user' in request.session:
        data = Add_Product.objects.get(pk=d)
        user = register.objects.get(email=request.session['user'])
        if whishlist.objects.filter(product_details_id=d).exists():
            return redirect(mywhishlist)

        else:
            whishlist.objects.create(product_details=data, user_details=user).save()
            messages.success(request, 'added to whishlist')
            return redirect(mywhishlist)
    return redirect(login)





def mywhishlist(re):
    if 'user' in re.session:
        user = register.objects.get(email=re.session['user'])
        data = whishlist.objects.filter(user_details=user)
        return render(re, 'mywhishlist.html',{'data': data,'user':user})
    return redirect(login)


def remove_whishlist(r,d):
    data=whishlist.objects.get(pk=d)
    data.delete()
    return redirect(mywhishlist)



def display(request):
    return render(request, 'display.html')


def manageproduct(request):
    data = Add_Product.objects.all()
    return render(request, 'manageproduct.html', {'data': data})
    # return redirect(user_logout)

def view_user(request):
    data =register.objects.all()
    return render(request, 'viewuser.html', {'data': data})


def delete_product(request, d):
    data = Add_Product.objects.get(pk=d)
    data.delete()
    messages.success(request, "Deleted Successfully")
    return redirect(manageproduct)


def update(request, g):
    data = Add_Product.objects.get(pk=g)
    if request.method == "POST":
        a = request.POST['n1']
        b = request.POST['n2']
        c = request.POST['n3']
        d = request.POST['n4']
        Add_Product.objects.filter(pk=g).update(ProductName=a, Price=b, Models=c, Category=d)
        messages.success(request, 'update successfully')
        return redirect(manageproduct)
    return render(request,'update.html',{'data':data})



def increments(request, d):
    if 'user' in request.session:
        data = cart.objects.get(pk=d)
        data.quantity+=1
        data.total_price=data.quantity*data.product_details.Price
        data.save()
        return redirect(mycart)


def decrements(request, d):
    if 'user' in request.session:
        data = cart.objects.get(pk=d)
        if data.quantity > 1:
            data.quantity -= 1
            data.save()
        else:
            return rem(request, d)

    return redirect(mycart)


def rem(request, d):
    data = cart.objects.get(pk=d)
    data.delete()
    messages.success(request, "deleted succesfully")
    return redirect(mycart)




def Birthday(r):
    data=Add_Product.objects.filter(Category='Birthday Cake')
    return render(r, 'birthday.html',{'data':data})



def wedding(r):
    data=Add_Product.objects.filter(Category='wedding Cake')
    return render(r, 'wedding.html',{'data':data})










# def forgot_password(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         try:
#             user = register.objects.get(email=email)
#         except:
#             messages.info(request, "Email id not registered")
#             return redirect(forgot_password)
#         # Generate and save a unique token
#         token = get_random_string(length=4)
#         PasswordReset.objects.create(user=user, token=token)
#
#         # Send email with reset link
#         reset_link = f'http://127.0.0.1:8000/reset/{token}'
#         try:
#             send_mail('Reset Your Password', f'Click the link to reset your password: {reset_link}',
#                       'settings.EMAIL_HOST_USER', [email], fail_silently=False)
#             # return render(request, 'email sent.html')
#         except:
#             messages.info(request, "Network connection failed")
#             return redirect(forgot_password)
#
#     return render(request,'forgot.html')


# def reset_password(request,token):
#     # Verify token and reset the password
#     print(token)
#     password_reset = PasswordReset.objects.get(token=token)
#     user = User.objects.get(id=password_reset.user_id)
#     if request.method == 'POST':
#         new_password = request.POST.get('newpassword')
#         repeat_password = request.POST.get('cpassword')
#         if repeat_password == new_password:
#             password_reset.user.password=new_password
#             password_reset.user.save()
#             # password_reset.delete()
#             return redirect(login)
#     return render(request, 'resetpassword.html', {'token': token})






def profile(re):
    if 'user' in re.session:
        data=register.objects.get(username=re.session['user'])
        return render(re, 'profile.html',{'d':data} )

def dboy_profile(r):
    data=dboy.objects.get(email=r.session['boy'])
    return render(r, 'dboy_profile.html', {'data': data})

def update_profile(r):
    if 'boy' in r.session:
        data = dboy.objects.get(email=r.session['boy'])
        print(data)
        product=update12(instance=data)
        if r.method=='POST':
            product=update12(r.POST,r.FILES,instance=data)
            if product.is_valid():
                product.save()
                return redirect(dboy_profile)
            return render(r,'update_profile.html',{'product':product})
    return render(r, 'update_profile.html')





# def logout(a):
#     a.session.flush()
#     return redirect(login)

def user_logout(r):
    if 'user' in r.session:
        r.session.flush()
        return redirect(user_login)

# def user_logout(r):
#     if 'user' in r.session:
#         r.session.delete()
#         return redirect(user_login)
#     return redirect(user_login)
def admin_logout(r):
    if 'admin' in r.session:
        r.session.flush()
        return redirect(admin_login)
def dboy_logout(r):
    if 'boy' in r.session:
        r.session.flush()
        return redirect(dboy_login)
    # return redirect(user_login)



order_list1=[]
def single_checkout(r,d):
    data=Add_Product.objects.get(pk=d)
    user=register.objects.get(email=r.session['user'])
    print(r.session['user'])
    order_list = {}
    if r.method=="POST":
        a = r.POST['n1']
        r.session['address'] = a
        b = r.POST['n2']
        r.session['city'] = b
        c = r.POST['n3']
        r.session['district'] = c
        d1 = r.POST['n4']
        r.session['pincode'] = d1
        e = r.POST['n5']
        r.session['state']=e
        f=r.POST['n6']
        g=r.POST['n7']
        r.session['total_price']=g
        order_list={'user_details':user.username,'house_name':a,'city':b,'district':c,'pincode':d1,'state':e,'product_name':f,'price':g}
        order_list1.append(order_list)
        return redirect(payment)
    return render(r,'single_checkout.html',{'data':data})

def payment(r):
    user=register.objects.get(email=r.session['user'])
    return render(r,'payment.html',{'order_list1':order_list1,'user':user})

import razorpay
def pay_razor(request, a):
    amount = order_list1[0]['price']
    x=int(amount)
    a=x*100
    user=register.objects.get(email=request.session['user'])
    order_currency = 'INR'
    client = razorpay.Client(
    auth=("rzp_test_SROSnyInFv81S4", "WIWYANkTTLg7iGbFgEbwj4BM"))
    payment=client.order.create({'amount': amount, 'currency': 'INR', 'payment_capture': '1'})
    order_details.objects.create(user_details=user,product_details=order_list1[0]['product_name'],
                                 total_price=order_list1[0]['price'],payment_status='PAID',address=order_list1[0]['house_name'],address_city=order_list1[0]['city'],
                                 address_district=order_list1[0]['district'],address_state=order_list1[0]['state'],address_pincode=order_list1[0]['pincode'])
    return render(request,"pay_razor.html",{'r':a})

def success(request):
    user = register.objects.get(email=request.session['user'])
    c = cart.objects.filter(user_details=user)
    for i in c:
        order_details.objects.create(user_details=user, product_details=i.product_details.ProductName,
                                     qunatity=i.quantity,
                                     total_price=request.se['total_price'], payment_status='PAID',
                                     address=request.session['address'], address_city=request.session['city'],
                                     address_district=request.session['district'],
                                     address_state=request.session['state'],
                                     address_pincode=request.session['pincode']).save()
    c.delete()
    return redirect(myorders)


def successs(request):
    user = register.objects.get(email=request.session['user'])
    c = cart.objects.filter(user_details=user)
    for i in c:
        order_details.objects.create(user_details=user, product_details=i.product_details.ProductName,
                                     qunatity=i.quantity,
                                     total_price=request.session['total_price'], payment_status='PAID',
                                     address=request.session['address'], address_city=request.session['city'],
                                     address_district=request.session['district'],
                                     address_state=request.session['state'],
                                     address_pincode=request.session['pincode']).save()
    c.delete()
    return redirect(myorders)



order_list2=[]
def cart_checkout(r):
    # data=add_product.objects.get(pk=d)
    user=register.objects.get(email=r.session['user'])
    data1=cart.objects.filter(user_details=user)
    quantity=data1.count()
    r.session['quantity']=quantity
    total_price=0
    for i in data1:
        a=i.product_details.Price
        b=i.quantity
        c=a*b
        total_price+=c
    print(total_price)
    r.session['total_price']=total_price
    print(quantity)
    if r.method=="POST":
        a=r.POST['n1']
        r.session['address']=a
        b=r.POST['n2']
        r.session['city'] = b
        c=r.POST['n3']
        r.session['district'] = c
        d1=r.POST['n4']
        r.session['pincode'] = d1
        e=r.POST['n5']
        r.session['state'] = e
        f=r.POST['n6']
        g=r.POST['n7']
        h=r.POST['n8']

        # order_list={'user_details':user.username,'house_name':a,'city':b,'district':c,'pincode':d1,'state':e,'product_name':f,'quantity':quantity,'total_price':total_price}
        # order_list2.append(order_list)
        print(order_list2)
        return redirect(cart_payment)
    return render(r,'cart_checkout.html',{'data1':data1})


def cart_payment(r):
    user=register.objects.get(email=r.session['user'])
    data=cart.objects.filter(user_details=user)
    print(data)
    return render(r,'cart_payment.html',{'order_list2':order_list2,'user':user,'data':data})



def cart_pay_razor(request, a):
    amount = request.session['total_price']
    x=int(amount)
    a=x*100
    order_currency = 'INR'
    client = razorpay.Client(
        auth=("rzp_test_SROSnyInFv81S4", "WIWYANkTTLg7iGbFgEbwj4BM"))
    payment = client.order.create({'amount': amount, 'currency': 'INR', 'payment_capture': '1'})
    # user=register.objects.get(email=request.session['user'])
    # c = cart.objects.filter(user_details=user)
    # for i in c:
    #     order_details.objects.create(user_details=user, product_details=i.product_details.name,
    #                                  qunatity=i.quantityy,
    #                                  total_price=i.total_price, payment_status='PAID',
    #                                  address=request.session['address'], address_city=request.session['city'],
    #                                  address_district=request.session['district'], address_state=request.session['state'],
    #                                  address_pincode=request.session['pincode']).save()
    # c.delete()
    return render(request,"cart_pay_razor.html",{'r':a})




def myorders(r):
    if 'user' in r.session:
        user=register.objects.get(email=r.session['user'])
        data=order_details.objects.filter(user_details=user)
        # data=order_details.objects.all()
    return render(r,'myorders.html',{'data':data})



def bookingdetails(r):
    data=order_details.objects.all()
    data1=dboy.objects.filter(work_status='free')
    if r.method=='POST':
        a=r.POST['n1']
        b=r.POST['n2']
        data2 = order_details.objects.filter(pk=a).update(dboy_name=b)
        return redirect(bookingdetails)
    return render(r, 'bookingdetails.html', {'data': data,'data1':data1})

def sendto_dboy(r,d,x):
    data=order_details.objects.filter(pk=d).update(dboy_name=x)
    return redirect(bookingdetails)


def order_requests(r):
    if 'boy' in r.session:
        data=dboy.objects.get(email=r.session['boy'])
        data1=order_details.objects.filter(dboy_name=data.name)
    return render(r,'order_requests.html',{'data':data,'data1':data1})
def delivery_details(r):
    if 'boy' in r.session:
        data=dboy.objects.get(email=r.session['boy'])
        data1=order_details.objects.filter(dboy_name=data.name)
    return render(r,'delivery_details.html',{'data':data,'data1':data1})
def accept_order(r,d):
    order_details.objects.filter(pk=d).update(delivery_status='accepted')
    return redirect(order_requests)

def reject_order(r,d):
    order_details.objects.filter(pk=d).update(delivery_status='rejected')
    return redirect(order_requests)

def order_delivered(r,d):
    order_details.objects.filter(pk=d).update(delivery_status='delivered')
    return redirect(delivery_details)



def myaddress(r):
    data=register.objects.get(email=r.session['user'])
    return render(r,'myaddress.html',{'data':data})

def updateaddress(r):
    data=register.objects.get(email=r.session['user'])
    if r.method=="POST":
        a=r.POST['n1']
        register.objects.filter(email=r.session['user']).update(address=a)
    return render(r,'updateaddress.html',{'data':data})


#
# from django.utils.crypto import get_random_string
# from django.core.mail import send_mail
# def forgot_password_user(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         try:
#             user = register.objects.get(email=email)
#         except:
#             messages.info(request, "Email id not registered")
#             return redirect(forgot_password_user)
#         # Generate and save a unique token
#         token = get_random_string(length=4)
#         PasswordResetUser.objects.create(user=user, token=token)
#
#         # Send email with reset link
#         reset_link = f'http://127.0.0.1:8000/reset_password_user/{token}'
#         try:
#             send_mail('Reset Your Password', f'Click the link to reset your password: {reset_link}',
#                       'settings.EMAIL_HOST_USER', [email], fail_silently=False)
#             # return render(request, 'emailsent.html')
#         except:
#             messages.info(request, "Network connection failed")
#             return redirect('forgot_password_user')
#
#     return render(request,'forgot_password_user.html')
#
# def reset_password_user(request,token):
#     # Verify token and reset the password
#     print(token)
#     password_reset = PasswordResetUser.objects.get(token=token)
#     # usr = User.objects.get(id=password_reset.user_id)
#     if request.method == 'POST':
#         new_password = request.POST.get('newpassword')
#         repeat_password = request.POST.get('cpassword')
#         if repeat_password == new_password:
#             password_reset.user.password=new_password
#             password_reset.user.save()
#             # password_reset.delete()
#             return redirect(user_login)
#     return render(request, 'reset_password_user.html', {'token': token})
#
#
# def forgot_password_dboy(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         try:
#             user = register.objects.get(email=email)
#         except:
#             messages.info(request, "Email id not registered")
#             return redirect(forgot_password_dboy)
#         # Generate and save a unique token
#         token = get_random_string(length=4)
#         PasswordResetDboy.objects.create(user=user, token=token)
#
#         # Send email with reset link
#         reset_link = f'http://127.0.0.1:8000/reset_password_dboy/{token}'
#         try:
#             send_mail('Reset Your Password', f'Click the link to reset your password: {reset_link}',
#                       'settings.EMAIL_HOST_USER', [email], fail_silently=False)
#             # return render(request, 'emailsent.html')
#         except:
#             messages.info(request, "Network connection failed")
#             return redirect(forgot_password_dboy)
#
#     return render(request,'forgot_password_dboy.html')
#
# def reset_password_dboy(request,token):
#     # Verify token and reset the password
#     print(token)
#     password_reset = PasswordResetDboy.objects.get(token=token)
#     # usr = User.objects.get(id=password_reset.user_id)
#     if request.method == 'POST':
#         new_password = request.POST.get('newpassword')
#         repeat_password = request.POST.get('cpassword')
#         if repeat_password == new_password:
#             password_reset.user.password=new_password
#             password_reset.user.save()
#             # password_reset.delete()
#             return redirect(dboy_login)
#     return render(request, 'reset_password_dboy.html', {'token': token})