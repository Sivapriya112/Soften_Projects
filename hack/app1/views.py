from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import *
from .forms import *
import razorpay
from django.utils.crypto import get_random_string # type: ignore
from django.core.mail import send_mail # type: ignore

# Create your views here.
def index(re):
    return render(re,'index_demo.html')

def reg(request):
    if request.method == 'POST':
        a = request.POST['z1']
        b = request.POST['z2']
        c = request.POST['z3']
        d = request.POST['z4']
        e = request.POST['z5']
        f = request.POST['z6']

        if user_register.objects.filter(username=d).exists():
            messages.error(request,'Username Already Exist')
        elif user_register.objects.filter(email=b).exists():
            messages.error(request,'Email Already Exist')
        else:
            user_register.objects.create(name=a, email=b, phone=c, username=d, password=e).save()
            messages.success(request,'Register Successfully')
            return render(request,'user_register.html')
    return render(request,'user_register.html')

def delivery_reg(request):
    if request.method == 'POST':
        a = request.POST['z1']
        b = request.POST['z2']
        c = request.POST['z3']
        d = request.POST['z4']
        e = request.POST['z5']
        f = request.POST['z6']
        g = request.POST['z7']

        if delivery_boy_register.objects.filter(username=e).exists():
            messages.error(request,'Username Already Exist')
        elif delivery_boy_register.objects.filter(email=b).exists():
            messages.error(request,'Email Already Exist')
        else:
            delivery_boy_register.objects.create(name=a, email=b, phone=c, driving_license_no=d, username=e, password=f).save()
            messages.success(request,'Register Successfully')
            return render(request,'delivery_boy_register.html')
    return render(request,'delivery_boy_register.html')

def delivery_login(request):
    if request.method =='POST':
        a = request.POST['x1']
        b = request.POST['x2']
        data=delivery_boy_register.objects.get(username=a)
        if data.password==b:
            if data.status == 'Accepted':
                request.session['delivery']=a
                messages.success(request,'Login success')
                return redirect(delivery_home)
            else:
                messages.error(request,'Request Pending')
                return redirect(delivery_login)
        else:
            messages.error(request, 'Incorect password')
            return redirect(delivery_login)
    return render(request, 'delivery_boy_login.html')

def delivery_home(request):

    return render(request, 'delivery_home.html',)
def booking(request):
    data = orders.objects.all()
    deliver=delivery_boy_register.objects.filter(work_status='Free',status='Accepted')
    return render(request,'booking_details.html',{'data':data,'deliver':deliver})

def delivery_view(request):
    data = delivery_boy_register.objects.all()
    return render(request, 'delivery_views.html', {'data': data})
def reject(request,a):
    data = delivery_boy_register.objects.get(pk=a)
    data.status='Rejected'
    data.save()
    return redirect(delivery_view)
def accept(request,a):
    data = delivery_boy_register.objects.get(pk=a)
    data.status = 'Accepted'
    data.save()
    return redirect(delivery_view)
def delivered(request,a):
    data = orders.objects.get(pk=a)
    data.product_status ='Delivered'
    data.save()
    delivery=delivery_boy_register.objects.get(username=request.session['delivery'])
    delivery.work_status='Free'
    delivery.save()
    messages.success(request,'You Have delivered the order.now you are Free')
    return redirect(delivery_order)

def choose(request,a):
    if request.method =='POST':
        b = request.POST['x1']
        data = orders.objects.get(pk=a)
        data.delivery_boy=b
        data.product_status='Out for delivery'
        data.save()
        try:
            d=delivery_boy_register.objects.get(username=b)
            d.work_status='Busy'
            d.save()
            # return redirect(booking)
        except Exception as e:
            print(e)
            messages.error(request,'Delivery Boy Doesnot Exist')
            return redirect(booking)
        messages.success(request,f'The order has been assigned for {b}')
        return redirect(booking)

def delivery_order(request):
    if 'delivery' in request.session:
        data=orders.objects.filter(delivery_boy=request.session['delivery'])
        return render(request,'delivery_orders.html',{'data':data})
    else:
        return redirect(login)

def login(request):
    if request.method =='POST':
        a = request.POST['x1']
        b = request.POST['x2']
        x = 'admin'
        y = '123'
        try:
            data=user_register.objects.get(username=a)
            if data.password==b:
                request.session['user']=a
                messages.success(request,'Login Success')
                return redirect(userhome)
            else:
                messages.error(request,'Incorrect password')
                return redirect(login)
        except:
            if a == x and b == y:
                request.session['admin']=a
                return redirect(adminhome)
            else:
                messages.error(request,'Incorrect password')
    return render(request,'login.html')



def adminhome(request):
    return  render(request,'admin_home.html')

def addproduct(request):
    if request.method == "POST":
        a = request.POST['a1']
        b = request.POST['a2']
        c = request.POST['a3']
        d = request.FILES['a4']
        add_product.objects.create(name=a, price=b, quantity=c, image=d).save()
    return render(request,'add_product.html')

def manageproduct(request):
    data=add_product.objects.all()
    return render(request,'manage_product.html',{'data':data})

def delete(request,a):
    data=add_product.objects.get(pk=a)
    data.delete()
    return redirect(manageproduct)

def update(request,a):
    data=add_product.objects.get(pk=a)
    m = modelform(instance=data)
    if request.method == 'POST':
        m = modelform(request.POST,request.FILES,instance=data)
        if m.is_valid():
            m.save()
            return redirect(manageproduct)
    return render(request,'update.html',{'data1':m})

def userhome(request):
    return render(request,'user_home.html')
def products(request):
    data=add_product.objects.all()
    return  render(request,'product.html',{'data':data})

def add_cart(request,d):
    pro=add_product.objects.get(pk=d)
    if cart.objects.filter(product_details=pro).exists():
        messages.error(request,'Item Already Added To Cart')
        return redirect(products)
    else:
        user=user_register.objects.get(username=request.session['user'])
        if pro.quantity < 1:
            messages.error(request,'Out Of stock')
            return redirect(products)
        else:
            cart.objects.create(user_details=user,product_details=pro,total_price=pro.price).save()
            messages.success(request,'Item Added to Your Cart')
            return redirect(products)

def wish(request,d):
    pro = add_product.objects.get(pk=d)
    if wishlist.objects.filter(product_details=pro).exists():
        messages.error(request,'Item Already Added To Wishlist')
        return redirect(products)
    else:
        user=user_register.objects.get(username=request.session['user'])
        wishlist.objects.create(user_details=user,product_details=pro).save()
        messages.success(request,'Item Added To Your Wishlist')
        return redirect(products)
def wish_view(request):
    user = user_register.objects.get(username=request.session['user'])
    data = wishlist.objects.filter(user_details=user)
    return render(request,'wishlist.html',{'data':data})

def cart_view(request):
    user=user_register.objects.get(username=request.session['user'])
    data=cart.objects.filter(user_details=user)
    total=0
    quantity=0
    for i in data:
        total+=i.total_price
        quantity+=1
    return render(request,'cart.html',{'data':data,'total':total,'quantity':quantity})
def address(request):
    user = user_register.objects.get(username=request.session['user'])
    if request.method == 'POST':
        x=request.POST['x1']
        y=request.POST['x2']
        z=request.POST['x3']
        a = request.POST['x4']
        b = request.POST['x5']
        c = request.POST['x6']
        d = request.POST['x7']
        e = request.POST['x8']
        user.name=x
        user.email=y
        user.phone=z
        user.pincode=a
        user.state=b
        user.city=c
        user.building_name=d
        user.road_name=e
        user.save()
        messages.success(request,'Address Added successfully')
        return redirect(order_sum)
    return render(request,'address.html',{'user':user})
def order_sum(request):
    user=user_register.objects.get(username=request.session['user'])
    data=cart.objects.filter(user_details=user)
    total = 0
    quantity = 0
    for i in data:
        total += i.total_price
        quantity += 1
    return render(request, 'Order_summary.html', {'data': data, 'total': total, 'quantity': quantity,'user':user })
def inc(request,d):
    data=cart.objects.get(pk=d)
    if data.quantity < data.product_details.quantity:
        data.quantity+=1
        data.total_price=data.quantity*data.product_details.price
        data.save()
    else:
        messages.error(request,'Out oF stock')
        return redirect(cart_view)
    return redirect(cart_view)
def dec(request,d):
    data=cart.objects.get(pk=d)
    if data.quantity>1 :
        data.quantity -= 1
        data.total_price=data.quantity*data.product_details.price
        data.save()
        return redirect(cart_view)
    else:
        data.delete()
        return redirect(cart_view)
def rem(request,d):
    data=cart.objects.get(pk=d)
    data.delete()
    return redirect(cart_view)


def remo(request,d):
    data=wishlist.objects.get(pk=d)
    data.delete()
    return redirect(wish_view)

# def order_view(request):
#     user = user_register.objects.get(username=request.session['user'])
#     pro =
#     orders.objects.create(user_details=user, product_details=).save()
def payment(request, id):
    amount = id*100
    order_currency = 'INR'
    client = razorpay.Client(
        auth=("rzp_test_SROSnyInFv81S4", "WIWYANkTTLg7iGbFgEbwj4BM"))
    payment = client.order.create({'amount': amount, 'currency': 'INR', 'payment_capture': '1'})
    return render(request, "payment.html",{'amount':amount,'id':id})

def order(request):
    user = user_register.objects.get(username=request.session['user'])
    data = cart.objects.filter(user_details=user)
    import datetime
    d = datetime.datetime.now()
    for i in data:
        a=add_product.objects.get(name=i.product_details.name)
        a.quantity=a.quantity-i.quantity
        print(a.quantity)
        a.save()
        orders.objects.create(user_details=user,product_details=a,quantity=i.quantity,amount=i.total_price,order_date=d).save()
    data.delete()
    return render(request,"success.html")

def myorder(request):
    user = user_register.objects.get(username=request.session['user'])
    data = orders.objects.filter(user_details=user)
    return render(request,'myorders.html',{'data':data})

def alert(request):
    low_stock_products = add_product.objects.filter(quantity__lt=5)
    return render(request, "alerts.html", {'low_stock_products':low_stock_products})

def history(request):
    user = delivery_boy_register.objects.get(username=request.session['delivery'])
    data = orders.objects.filter(product_status='Delivered',delivery_boy=user.username)
    return render(request,'order_history.html',{'data':data})
def profile(request):
    data = delivery_boy_register.objects.get(username=request.session['delivery'])
    return render(request,'profile.html',{'data':data})

def logout(request):
    if 'user' in request.session or 'admin' in request.session:
        request.session.flush()
        return redirect(login)
    return redirect(login)
def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = user_register.objects.get(email=email)
        except Exception as e:
            print (e)# noqa: E722
            messages.info(request, "Email id not registered")
            return redirect(forgot_password)
        # Generate and save a unique token
        token = get_random_string(length=4)
        PasswordReset.objects.create(user_details=user, token=token)

        # Send email with reset link
        reset_link = f'http://127.0.0.1:8000/reset_password/{token}'
        try:
            send_mail('Reset Your Password', f'Click the link to reset your password: {reset_link}',
                      'settings.EMAIL_HOST_USER', [email], fail_silently=False)
            # return render(request, 'emailsent.html')
        except:  # noqa: E722
            messages.info(request, "Network connection failed")
            return redirect(forgot_password)

    return render(request,'forgot.html')

def reset_password(request,token):
    # Verify token and reset the password
    print(token)
    password_reset = PasswordReset.objects.get(token=token)
    # usr = User.objects.get(id=password_reset.user_id)
    if request.method == 'POST':
        new_password = request.POST.get('newpassword')
        repeat_password = request.POST.get('cpassword')
        if repeat_password == new_password:
            password_reset.user_details.password=new_password
            password_reset.user_details.save()
            # password_reset.delete()
            return redirect(login)
    return render(request, 'reset_password.html', {'token': token})
def about(request):
    return  render(request,'about-us.html')

def contact(request):
    return  render(request,'contact.html')

def blog(request):
    return  render(request,'blog.html')