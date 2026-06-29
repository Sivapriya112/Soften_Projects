import random
from django.shortcuts import redirect, render # type: ignore
from django.http import HttpResponse  # noqa: F401 # type: ignore
from datetime import datetime
from django.contrib import messages # type: ignore
from django.contrib import messages  # type: ignore # noqa: F811
from django.shortcuts import redirect, render
from django.core.exceptions import ObjectDoesNotExist
from .form import SampleForm,user_address,user_profile,DBoyDetails,ProductImageForm,ProductForm,ServiceForm # type: ignore # noqa: F811
from .models import user_details,services,BookingOrders,PasswordReset,Products,UserWishlist,UserCarts,ProductsOrders,DeliveryBoy,DPasswordReset,ProductRate # noqa: F403
import razorpay   # type: ignore # noqa: E402
from django.utils.crypto import get_random_string # type: ignore
from django.core.mail import send_mail # type: ignore
import re
from django.conf import settings
from django.contrib.auth import authenticate, login




# Create your views here.

def index(request):
    products = Products.objects.all()
    service = services.objects.all()
    return render(request,'index.html',{'products':products,'services':service})


def UserRegister(request):
    return render(request, 'user/booking/User_register.html')


def user_register(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phoneno']
        username = request.POST['username']
        password = request.POST['password']
        cpassword = request.POST['cpassword']
        
        
        data = user_details.objects.filter(username=username)
        if data.exists():
            messages.error(request, 'User already exists')
            return redirect(UserRegister)  
        
        data = user_details.objects.filter(email=email)
        if data.exists():
            messages.error(request, 'User with email already exists')
            return redirect(UserRegister) 
        data = user_details.objects.filter(phone_no=phone)
        if data.exists():
            messages.error(request, 'User with phone number already exists')
            return redirect(UserRegister) 
        if password == cpassword:
            user = user_details(name=name, email=email, phone_no=phone, username=username,password=password)
            user.save()
            return render(request, 'user/booking/User_login.html')
        else:
            messages.error(request, 'Passwords do not match')
            return redirect(UserRegister)  
            
    return redirect(UserRegister) 

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            data = user_details.objects.get(username=username)
            if password == data.password:
                if data.status == 'active':
                    request.session['user'] = username
                    return redirect(UserHome)
                messages.error(request, 'User is not approved to login')
            else:
                messages.error(request, 'Invalid Password')
        except user_details.DoesNotExist:
            messages.error(request, "Username not found")
        return redirect(user_login)
    return render(request, 'user/booking/user_login.html')

def UserHome(request):
    products = Products.objects.all()
    service = services.objects.all()
    
    return render(request,'user/booking/UserHome.html',{'user':request.session['user'],'products':products,'services':service})


def ServiceListing(request):
    if 'user' in request.session:
        data = services.objects.filter(status='approved')
        return render(request,'user/booking/ServiceListing.html',{'user':request.session['user'],'data':data})
    else:
        messages.error(request, 'Login First to Explore Services')
        return redirect(index)

def UserServices(request):
    data = services.objects.filter(status='approved')
    print(data)
    return render(request,'user/booking/ServiceListing.html',{'user':request.session['user'],'data':data})

def Userbooking(request, i):
    data = services.objects.get(pk=i)
    print(data.service_name)
    datas = services.objects.filter(status='approved')

    # time_slots = list(range(9, 22))  # 9 to 21 inclusive
    context = {
        'user': request.session['user'],
        's': data.service_name,
        'services': datas,
        'data': data,
        'status':17
    }
    return render(request, 'user/booking/UserBooking.html', context)
    
def Userbooking2(request):
   
    datas = services.objects.all()

    # time_slots = list(range(9, 22))  # 9 to 21 inclusive
    context = {
        'user': request.session['user'],
        'services': datas,
        'status':17
    }
    return render(request, 'user/booking/UserBooking.html', context)
    

def logout(request):
    if 'user' in request.session:
        request.session.flush()
        return redirect(index)
    if 'duser' in request.session:
        request.session.flush()
    if 'admin' in request.session:
        request.session.flush()
    return redirect(index)





def timeslotbooking(request):
    if request.method == 'POST':
        # Get the selected services as a list of values
        user = user_details.objects.get(username=request.session['user'])
        selected_services = request.POST.getlist('services')
        if not selected_services:
            messages.error(request, 'Please select at least one service')
            return redirect(Userbooking2)
        c = len(selected_services)
        price = c * 100
        s = ','.join(selected_services)                                                                             
        print(s)
        
        # Get the other form fields
        service_date_str = request.POST.get('service_date')
        service_date = datetime.strptime(service_date_str, '%Y-%m-%d').date()
        car_model = request.POST.get('car_model')
        car_number = request.POST.get('car_number')
        if car_number:
            pattern = r"^[A-Z]{2}\d{2}[A-Z]{1,3}\d{1,4}$"
            if not re.match(pattern, car_number):
                messages.error(request, 'Enter a valid car number')
                return redirect(Userbooking2)   
        print(service_date)
        print("Service date:", service_date, "Type:", type(service_date))

        # Logic to check booked time slots for the selected date
        booked_slots = BookingOrders.objects.filter(date=service_date).values_list('time_slot', flat=True)
        print('booked_slots ----------')
        print(booked_slots)

        # Generate all possible time slots (9 AM to 10 PM)
        all_time_slots = [f"{hour:02}:00" for hour in range(9, 22)]

        # Adjust available slots for today's date
        now = datetime.now()
        if service_date == now.date():
            # Exclude past time slots if booking is for today
            current_hour = now.hour
            print(current_hour)
            print('=========')
            current_time_slot = f"{current_hour:02}:00"
            all_time_slots = [slot for slot in all_time_slots if slot > current_time_slot]

        # Filter available time slots by excluding booked slots
        available_time_slots = [slot for slot in all_time_slots if slot not in booked_slots]
        print("Available time slots:", available_time_slots)

        context = {
            'available_time_slots': available_time_slots,
            'user': user,
            'selected_services': s.strip(),
            'car_number': car_number,
            'car_model': car_model,
            'service_date': service_date,
            'price': price,
            'status': 50,
        }
        
        return render(request, 'user/booking/TimeSlot.html', context)




def order(request):
    if request.method == 'POST':
        user_detail = user_details.objects.get(username = request.session['user'])  # noqa: F823
        selected_services = request.POST['services']
        print("selected_services ------------")
        print(selected_services)
        car_model = request.POST['car_model']
        car_number = request.POST['car_number']
        if car_number:
            pattern = r"^[A-Z]{2}\d{2}[A-Z]{1,3}\d{1,4}$"
            if not re.match(pattern, car_number):
                messages.error(request,'Enter a valid car number')
                return redirect(Userbooking2)   
        date_str = request.POST['date']
        # date_obj = datetime.strptime(date_str, "%b. %d, %Y")  # Convert 'Nov. 15, 2024' to a datetime object
        date_obj = datetime.strptime(date_str, "%B %d, %Y")
        date = date_obj.strftime("%Y-%m-%d")  # Format the date as 'YYYY-MM-DD'

        time_slot = request.POST['timeSlot']
        print("Time slot ------------")
        print(time_slot)
        words = selected_services.split(',')
        word_count = len(words)
        amount = 100 * word_count * 100 * 100 # Convert to paise
        print('amount ------------')
        print(amount)
        price = amount / 10000
        new_booking=BookingOrders.objects.create(user=user_detail,services = selected_services,car_model = car_model,car_number = car_number,date = date,time_slot = time_slot,payment_amount = price)
        booking_id = new_booking.id
        # Store the booking ID in session
        request.session['booking_id'] = booking_id
        print("Booking id  -----------")
        print(request.session['booking_id'])
        
        order_currency = 'INR'  # noqa: F841
        client = razorpay.Client(
            auth=("rzp_test_SROSnyInFv81S4", "WIWYANkTTLg7iGbFgEbwj4BM"))
        payment = client.order.create({'amount': amount, 'currency':'INR', 'payment_capture':'1'})  # noqa: F841
        return render(request,'user/booking/payment.html',{'price':amount / 100,'status': 85,'p':amount/10000})
        
        


def success(request):
    # Get the booking ID from the session
    booking_id = request.session['booking_id']
    print('bid =======')
    print(booking_id)
    
    # Retrieve the booking order by ID
    booking_order = BookingOrders.objects.get(id=booking_id)
    print(booking_order)
    
    # Update the payment status
    booking_order.payment_status = 'completed'
    booking_order.save()
    
    # Fetch updated booking details
    booking_details = BookingOrders.objects.get(id=booking_id)
    
    # Send email to the user
    user_detail = user_details.objects.get(username = request.session['user'])  # noqa: F823
    user_email = user_detail.email # Assuming 'user' session contains the user's details
    
    subject = 'Your Appointment is Booked Successfully!'
    message = f"""
    Hello {user_detail.name},

    Your appointment has been successfully booked. Below are the details:
    
    Booking ID: {booking_details.id}
    Service: {booking_details.services}
    Booked Date: {booking_details.date}
    Time: {booking_details.time_slot}
    
    Payment Status: {booking_details.payment_status}
    
    Thank you for booking with us!

    Best regards,
    The Booking Team
    """
    
    send_mail(
        subject, 
        message, 
        settings.DEFAULT_FROM_EMAIL,  # From email address
        [user_email],  # To email address
        fail_silently=False,
    )
    
    # Render the invoice page
    return render(request, 'user/booking/invoice.html', {
        'user': request.session['user'],
        'order': booking_details
    })




def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = user_details.objects.get(email=email)
        except:  # noqa: E722
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

    return render(request,'user/booking/forgot.html')

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
            return redirect(user_login)
    return render(request, 'user/booking/reset_password.html', {'token': token})




def mark_expired_bookings(user):
    now = datetime.now()

    # Fetch all expired bookings with status 'Pending' for the logged-in user
    expired_bookings = BookingOrders.objects.filter(
        user=user,
        status='Pending',
        date__lt=now.date()  # Booking date is in the past
    ) | BookingOrders.objects.filter(
        user=user,
        status='Pending',
        date=now.date(),
        time_slot__lt=now.strftime('%H:%M')  # Time slot is in the past for today's bookings
    )

    # Update the status to 'Missed'
    expired_bookings.update(status='Missed')

def UserBookingListing(request):
    # Fetch the current user
    user = user_details.objects.get(username=request.session['user'])

    # Mark expired bookings as missed
    mark_expired_bookings(user)

    # Fetch completed bookings
    booking_details = BookingOrders.objects.filter(user=user).order_by('-created_at')
    c=[]
    pending = BookingOrders.objects.filter(user=user,payment_status= 'Pending')
    for i in pending:
        d={
            'pk': i.pk,
            'amount': i.payment_amount * 100
        }
        c.append(d)
    # Render the template
    return render(request, 'user/booking/UserBookingListing.html', {
        'user': request.session['user'],
        'booking_details': booking_details,
        'p':c
    })

from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect
from .models import BookingOrders

def CancelBooking(request, p):
    # Retrieve the booking order by primary key (ID)
    booking = BookingOrders.objects.get(pk=p)
    
    # Update the booking status to 'cancelled'
    booking.status = 'cancelled'
    booking.refund_status = 'pending'
    booking.save()

    user_detail = user_details.objects.get(username = request.session['user'])  # noqa: F823
    user_email = user_detail.email # Assuming 'user' session contains the user's details
    
    subject = 'Your Booking has been Cancelled'
    message = f"""
    Hello {user_detail.name},

    We regret to inform you that your booking with us has been cancelled. Below are the details:

    Booking ID: {booking.id}
    Service: {booking.services}
    Date: {booking.date}
    Time: {booking.time_slot}

    As per our policy, a refund will be processed to your account.

    We apologize for any inconvenience this may have caused. Please feel free to contact us if you have any questions.

    Best regards,
    The Booking Team
    """
    
    # Send the email
    send_mail(
        subject, 
        message, 
        settings.DEFAULT_FROM_EMAIL,  # From email address
        [user_email],  # To email address
        fail_silently=False,  # Ensure any errors in sending are raised
    )
    
    # Display a message to the user
    messages.info(request, 'Your booking has been cancelled. Payment will be refunded to your account.')

    # Redirect to the user's booking listing page
    return redirect(UserBookingListing)  # Assuming 'UserBookingListing' is the name of the view


def UserProfile(request):
    details= user_details.objects.get(username = request.session.get('user'))
    print(details.name, details.email, details.phone_no)  # Check updated fields
    if request.method == 'POST':
        s = user_profile(request.POST, request.FILES, instance=details)
        print('done  --- -- - ')
        
        if s.is_valid():
            s.save()
            print('done  --- -- - ')
            messages.info(request,'Details saved')
            return redirect(UserProfile)
        else:
            print(s.errors)
          
        
    s = user_profile(instance = details)
    return render(request,'user/booking/UserProfile.html',
                  {'user':request.session['user'],'details':s,'pk':details.pk})
    





#User products==========================================================================================================================================

def products_listing(request):
    data = Products.objects.all()
    user = user_details.objects.get(username=request.session['user'])
    wishlist = UserWishlist.objects.filter(user_details = user)
    request.session['quantity'] = 1
    wlist=[]
    for i in wishlist:
        wlist.append(i.product_details.pk)
    
    return render(request,'user/order_product/ProductsListing.html',{'user':request.session['user'],'data':data,'wlist':wlist})

def SellProducts(request):
    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        product_price = request.POST.get('price')
        product_details = request.POST.get('details')
        image = request.FILES.get('image')
        user = user_details.objects.get(username = request.session['user'])
        Products.objects.create(product_name=product_name, product_price=product_price, product_details=product_details, product_image = image)
        
        return redirect(YourProducts)
    return render(request,'user/order_product/SellProducts.html',{'user':request.session['user']})

def YourProducts(request):
    if 'user' in request.session:
        user = user_details.objects.get(username = request.session['user'])
        details = Products.objects.all()
        return render(request,'user/order_product/YourProducts.html',{'user':request.session['user'],'products':details,'flag':1})  
    return render(request,'user/booking/user_login.html',{'flag':1})  


def Edit(request,i):
    details = Products.objects.get(pk=i)
    if request.method == 'POST':
        s = SampleForm(request.POST, request.FILES, instance=details)
        print('done  --- -- - ')
        
        if s.is_valid():
            s.save()
            print('done  --- -- - ')
            return redirect(YourProducts)
        else:
            print(s.errors)
          
        
    s = SampleForm(instance = details)
    return render(request,'user/order_product/YourProducts.html',
                  {'user':request.session['user'],'products':s,'pk':details.pk,'flag':0})

def wishlist(request,i):
    user =user_details.objects.get(username = request.session['user'])
    product = Products.objects.get(pk=i)
    try:
        data = UserWishlist.objects.get(user_details=user, product_details=product)
        data.delete()
    except:
        UserWishlist.objects.create(user_details=user, product_details=product).save()
    return redirect(products_listing)
def ViewWishList(request):
    user =user_details.objects.get(username = request.session['user'])
    data = UserWishlist.objects.filter(user_details=user)
    return render(request,'user/order_product/ViewWishList.html',{'user':request.session['user'],'data':data})
    

def add_cart(request,i):
    user = user_details.objects.get(username = request.session['user'])
    product = Products.objects.get(pk=i)
    if product.quantity != 0: 
        try:
            c = UserCarts.objects.get(user_details=user, product_details=product)
            c.quantity = request.session.get('quantity')
            c.save()
        except:
            UserCarts.objects.create(user_details=user, product_details=product,quantity = request.session.get('quantity')).save()
        if messages is not None:
            messages.info(request,'Item added successfully')
    else:
        if messages is not None:
            messages.info(request,'Item Out of Stock')
    return redirect(product_details,i)
   
    
    
def product_details(request, i):
    if 'user' in request.session:
        user = user_details.objects.get(username=request.session['user'])
        details = Products.objects.get(pk=i)
        reviews = ProductRate.objects.filter(Product = details)
        # Initialize quantity in session if not already set
        if 'quantity' not in request.session:
            request.session['quantity'] = 1
        
        return render(request, 'user/order_product/ProductDetails.html', {
            'user': request.session['user'],
            'details': details,
            'quantity': request.session['quantity'],
            'reviews':reviews
        })
    else:
        messages.error(request, 'Login First to Explore Services')
        return redirect(user_login)
    




def increment(request, i):
    if 'user' in request.session:
        user = user_details.objects.get(username=request.session['user'])
        data = Products.objects.get(pk=i)
        
        # Safely get the quantity from session with a default value of 0
        current_quantity = request.session.get('quantity', 0)
        
        if data.quantity > current_quantity:
            request.session['quantity'] = current_quantity + 1
            messages.info(request, 'Item updated')
        else:
            messages.info(request, 'Item Out of Stock')

    return redirect(product_details, i)


def decrement(request, i):
    if 'user' in request.session:
        user = user_details.objects.get(username=request.session['user'])
        data = Products.objects.get(pk=i)
        
        # Safely get the quantity from session with a default value of 1
        current_quantity = request.session.get('quantity', 1)
        
        if current_quantity > 1:
            request.session['quantity'] = current_quantity - 1
            messages.info(request, 'Item updated')
        else:
            messages.info(request, 'Quantity cannot be less than 1')
            request.session.pop('quantity', None)  # Remove key if no items remain
            return redirect(products_listing)

    return redirect(product_details, i)

def user_cart(request):
    user = user_details.objects.get(username = request.session['user'])
    data = UserCarts.objects.filter(user_details=user)
    l=[]
    total_price =0
    for i in data:
        d={
            'p_pk':i.product_details.pk,
            'total_price':int(i.product_details.product_price) * i.quantity
        }
        l.append(d)
        print(d )
        print(l )
        total_price += d['total_price']
    return render(request, 'user/order_product/UserCarts.html',{'user':request.session['user'],'data':data,'list':l, 'total':total_price})

def cart_increment(request,i):
    if 'user' in request.session:
        user = user_details.objects.get(username = request.session['user'])
        data = UserCarts.objects.get(pk=i,user_details=user)
        data.quantity += 1
        
        data.save()
    return redirect(user_cart)
def cart_decrement(request,i):
    if 'user' in request.session:
        user = user_details.objects.get(username = request.session['user'])
        data = UserCarts.objects.get(pk=i,user_details=user)
        data.quantity -= 1
        
        
        data.save()
        if data.quantity == 0:
            UserCarts.objects.get(pk=i).delete()
    return redirect(user_cart)

def Yourorders(request):
    user = user_details.objects.get(username = request.session['user'])
    orders = ProductsOrders.objects.filter(user_details=user).order_by('-created_at')
    return render(request,'user/order_product/YourOrders.html',{'user':request.session['user'],'orders':orders})

def ProductsPayment(request,i):
    i*=100
    
    user = user_details.objects.get(username = request.session['user'])
    if request.method == 'POST':
        s = user_address(request.POST, request.FILES, instance=user)
        print('done  --- -- - ')
        
        if s.is_valid():
            s.save()
            print('done  --- -- - ')
            return render(request,'user/order_product/payment.html',{'user':request.session['user'],'details':s,'flag':0,'price':i,'p':int(i/100)})
        else:
            print(s.errors)
          
        
    s = user_address(instance = user)
    
    
    order_currency = 'INR'  # noqa: F841
    client = razorpay.Client(
         auth=("rzp_test_SROSnyInFv81S4", "WIWYANkTTLg7iGbFgEbwj4BM"))
    payment = client.order.create({'amount': i, 'currency':'INR', 'payment_capture':'1'})  # noqa: F841
    return render(request,'user/order_product/payment.html',{'user':request.session['user'],'details':s,'flag':1,'price':i,'p':int(i/100)})



def OrderSuccess(request):
    # Get the current user
    user = user_details.objects.get(username=request.session['user'])
    
    # Fetch all items in the user's cart
    data = UserCarts.objects.filter(user_details=user)  
    
    # Calculate total price
    total_price = 0
    for item in data:
        total_price += int(item.product_details.product_price) * item.quantity
    
    print(data)

    # Prepare the list of products and create orders
    ordered_products = []
    for item in data:
        product_total_price = int(item.product_details.product_price) * item.quantity
        

# Generate a random 4-digit number
        random_number = random.randint(1000, 9999)
        # Create a new order for each product in the cart
        ProductsOrders.objects.create(
            user_details=user,
            product_details=item.product_details,
            payment_amount=product_total_price,
            quantity=item.quantity,
            payment_status='success',
            product_code=random_number,created_at=datetime.now()
        )
        p = Products.objects.get(pk = item.product_details.pk)
        p.quantity -= item.quantity
        p.save()
        
        # Add product info to the ordered products list
        ordered_products.append({
            'product_name': item.product_details.product_name,
            'product_quantity': item.quantity,
            'total_price': product_total_price,
            'product_code':random_number
        })
    
    # Clear the user's cart after the order is placed
    UserCarts.objects.filter(user_details=user).delete()
    
    # Send the order confirmation email
    send_order_confirmation_email(user, ordered_products, total_price)

    # Send the payment receipt email
    # send_payment_receipt_email(user, total_price,ordered_products)
    
    # Render the invoice page
    return render(request, "user/order_product/ProductsInvoice.html", {
        'user': request.session['user'],
        'data': data,
        'list': ordered_products,
        'total': total_price,
        'address': user.housename,
        'landmark': user.landmark,
        'area': user.area,
        'pincode': user.pincode,
    })

def send_order_confirmation_email(user, ordered_products, total_price):
    # Email subject and body for the order confirmation
    subject = 'Your Order has been Confirmed!'
    
    product_details = ""
    
    # Loop through the ordered products and format the details
    for item in ordered_products:
        product_details += f"Product: {item['product_name']} | Quantity: {item['product_quantity']} | Total Price: ₹{item['total_price']} | Delivery Code: {item['product_code']}\n"
    
    # Prepare the message
    message = f"""
    Hello {user.name},

    Thank you for your order! Here are the details of the products you've ordered:

    {product_details}

    Total Price: ₹{total_price}

    We will notify you once your products are shipped.

    Best regards,
    The Shopping Team
    """
    
    try:
        # Send the email
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,  # From email address
            [user.email],  # To email address
            fail_silently=False,  # Ensure any errors in sending are raised
        )
        print("Email sent successfully")
    except Exception as e:
        print(f"Exception occurred while sending email: {e}")

        


def send_payment_receipt_email(user, total_price,ordered_products):
    # Email subject and body for the payment receipt
    subject = 'Your Payment Receipt'
    product_details =""
    for item in ordered_products:
        product_details += f"Product: {item['product'].product_name} | Quantity: {item['quantity']} | Total Price: ${item['total_price']}| Delivery Code: ${item['product_code']}\n"
    print("Total=",total_price)
    message = f"""
    Hello {user.name},

    We have successfully received your payment. Below are the details of your transaction:

    {product_details}
    

    Total Payment: ${total_price}

    Thank you for shopping with us! Your order will be processed shortly.

    Best regards,
    The Shopping Team
    """
    
    # Send the email
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,  # From email address
        [user.email],  # To email address
        fail_silently=False,  # Ensure any errors in sending are raised
    )

def BuyNow(request,i):
    user = user_details.objects.get(username = request.session['user'])
    request.session['product_id'] = i
    data =Products.objects.get(pk=i)
    product_price = data.product_price
    total = 0
    print('==========   =============================')
    print(request.session['product_id'])
    print(data)
    total = int(data.product_price) * int(request.session.get('quantity'))
    print(total)
    
    
    if request.method == 'POST':
        s = user_address(request.POST, request.FILES, instance=user)
        print('done  --- -- - ')
        
        if s.is_valid():
            s.save()
            print('done  --- -- - ')
            return render(request,'user/order_product/singlepayment.html',{'user':request.session['user'],'details':s,'flag':0,'price':product_price,'p':product_price,'data':data,'quantity':request.session.get('quantity')})
        else:
            print(s.errors)
          
        
    s = user_address(instance = user)
    
    
    order_currency = 'INR'  # noqa: F841
    client = razorpay.Client(
         auth=("rzp_test_SROSnyInFv81S4", "WIWYANkTTLg7iGbFgEbwj4BM"))
    payment = client.order.create({'amount': product_price, 'currency':'INR', 'payment_capture':'1'})  # noqa: F841
    
    return render(request,'user/order_product/singlepayment.html',{'user':request.session['user'],'details':s,'flag':1,'price':product_price,'p':product_price,'data':data,'quantity':request.session.get('quantity'),'total':total})

def SingleProductsPayment(request,i):
    i*=100
    
    user = user_details.objects.get(username = request.session['user'])
    if request.method == 'POST':
        s = user_address(request.POST, request.FILES, instance=user)
        print('done  --- -- - ')
        
        if s.is_valid():
            s.save()
            print('done  --- -- - ')
            return render(request,'user/order_product/singlepayment.html',{'user':request.session['user'],'details':s,'flag':0,'price':i,'p':int(i/100)})
        else:
            print(s.errors)
          
        
    s = user_address(instance = user)
    
    
    order_currency = 'INR'  # noqa: F841
    client = razorpay.Client(
         auth=("rzp_test_SROSnyInFv81S4", "WIWYANkTTLg7iGbFgEbwj4BM"))
    payment = client.order.create({'amount': i, 'currency':'INR', 'payment_capture':'1'})  # noqa: F841
    
    return render(request,'user/order_product/singlepayment.html',{'user':request.session['user'],'details':s,'flag':1,'price':i,'p':int(i/100)})

def SingleOrderSuccess(request):
     # Get the current user
    user = user_details.objects.get(username=request.session['user'])
    
    # Fetch all items in the user's cart
    data = Products.objects.get(pk=request.session['product_id'])  
    
    # Calculate total price
    total_price = int(data.product_price) * request.session['quantity']
    
    
    print(data)

    # Prepare the list of products and create orders
    

# Generate a random 4-digit number
    random_number = random.randint(1000, 9999)
    # Create a new order for each product in the cart
    details =ProductsOrders.objects.create(
        user_details=user,
        product_details=data,
        payment_amount=total_price,
        quantity=request.session['quantity'],
        payment_status='success',
        product_code=random_number,created_at=datetime.now())
    
    p = Products.objects.get(pk = data.pk)
    p.quantity -= request.session['quantity']
    p.save()
    
    # Add product info to the ordered products list
    ordered_products = []
    ordered_products.append({
        'product_name': data.product_name,
        'product_quantity': request.session['quantity'],
        'total_price': total_price,
        'product_code':random_number
    })
    
    
    
    # Send the order confirmation email
    send_order_confirmation_email(user, ordered_products, total_price)

    # Send the payment receipt email
    # send_payment_receipt_email(user, total_price,ordered_products)
    
    # Render the invoice page
    return render(request, "user/order_product/SingleProductInvoice.html", {
        'user': request.session['user'],
        'data': data,
        'details': details,
        'total': total_price,
        'address': user.housename,
        'landmark': user.landmark,
        'area': user.area,
        'pincode': user.pincode,
    })

def CancelOrder(request,i):
    order  = ProductsOrders.objects.get(pk=i)
    print(i)
    print('-----------------------------------')
    order.order_status = 'cancelled'
    order.refund_status = 'pending'
    order.save()
    messages.info(request,"Order cancelled ")
    return redirect(Yourorders)

def Rate(request):
    
    if  request.method == 'POST':
        user = user_details.objects.get(username = request.session.get('user'))
        print(request.POST.get('id'))
        print('-----------------')
        product = Products.objects.get(pk = request.POST.get('id'))
        
        rating = request.POST.get('userRating')
        feedback = request.POST.get('userFeedback')
        print('===============================')
        print(product)
        print(rating)
        print(product)
            
        print(user)
        try:
            data = ProductRate.objects.get(User = user, Product = product)
            data.rate = rating
            data.feedback = feedback
            data.save()
            messages.success(request,f'You Rated {data.Product.product_name}')
        except ProductRate.DoesNotExist:
            data = ProductRate.objects.create(User = user, Product = product, rate = rating, feedback = feedback)
            messages.success(request,f'You Rated {data.Product.product_name}')
    
    return redirect(Yourorders)



#================================================Delivery Boy ======================================================================================

def DUserHome(request):
    data = DeliveryBoy.objects.get(username=request.session['duser'])
    if data.status == 'not approved':
        messages.info(request,'Your are not approved by Admin.')
        
    elif data.status == 'rejected':
        messages.info(request,'Your are Rejected by Admin.')
        

        
        
    return render(request, "DeliveryBoy/DUserHome.html", {'duser': request.session['duser']})

def DUserProfile(request):
    details= DeliveryBoy.objects.get(username = request.session.get('duser'))
    print(details.name, details.email, details.phone)  # Check updated fields
    if request.method == 'POST':
        s = DBoyDetails(request.POST, request.FILES, instance=details)
        print('done  --- -- - ')
        
        if s.is_valid():
            s.save()
            print('done2  --- -- - ')
            messages.info(request,'Details saved')
            return redirect(DUserProfile)
        else:
            print(s.errors)
          
        
    s = DBoyDetails(instance = details)
    return render(request,'DeliveryBoy/DUserProfile.html',{'duser':request.session['duser'],'details':s})

def DUserRegister(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phoneno']
       
        l_no = request.POST['License_number']
        image = request.FILES['License_image']
        username = request.POST['username']
        password = request.POST['password']
        cpassword = request.POST['cpassword']
        print('================================================================')
        
        data = DeliveryBoy.objects.filter(username=username)
        if data.exists():
            messages.error(request, 'User already exists')
            return redirect(DUserRegister)  
        data = DeliveryBoy.objects.filter(email=email)
        if data.exists():
            messages.error(request, 'User with email already exists')
            return redirect(DUserRegister) 
        data = DeliveryBoy.objects.filter(phone=phone)
        if data.exists():
            messages.error(request, 'User with phone number already exists')
            return redirect(DUserRegister) 
        data = DeliveryBoy.objects.filter(license_number=l_no)
        if data.exists():
            messages.error(request, 'User with license number already exists')
            return redirect(DUserRegister) 
        if password == cpassword:
            user = DeliveryBoy(name=name, email=email, phone=phone, username=username,password=password,license_image = image,license_number = l_no)
            user.save()
            return render(request, 'DeliveryBoy/DUserLogin.html')
        else:
            messages.error(request, 'Passwords do not match')
            return redirect(DUserRegister)  
            
    return render(request,'DeliveryBoy/DUserRegister.html') 

def DUserLogin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            data = DeliveryBoy.objects.get(username = username)
            if password == data.password:
                request.session['duser'] = username
                return redirect(DUserHome)
            else:
                messages.error(request,'Invalid Password')
                return redirect(DUserLogin)
        except Exception:
            messages.error(request,"Username not found")
            return redirect(DUserLogin)
    else:
        return render(request,'DeliveryBoy/DUserLogin.html')


def Dforgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = DeliveryBoy.objects.get(email=email)
        except:  # noqa: E722
            messages.info(request, "Email id not registered")
            return redirect(forgot_password)
        # Generate and save a unique token
        token = get_random_string(length=4)
        DPasswordReset.objects.create(user_details=user, token=token)

        # Send email with reset link
        reset_link = f'http://127.0.0.1:8000/Dreset_password/{token}'
        try:
            send_mail('Reset Your Password', f'Click the link to reset your password: {reset_link}',
                      'settings.EMAIL_HOST_USER', [email], fail_silently=False)
            # return render(request, 'emailsent.html')
        except:  # noqa: E722
            messages.info(request, "Network connection failed")
            return redirect(Dforgot_password)

    return render(request,'DeliveryBoy/Dforgot.html')

def Dreset_password(request,token):
    # Verify token and reset the password
    print(token)
    password_reset = DPasswordReset.objects.get(token=token)
    # usr = User.objects.get(id=password_reset.user_id)
    if request.method == 'POST':
        new_password = request.POST.get('newpassword')
        repeat_password = request.POST.get('cpassword')
        if repeat_password == new_password:
            password_reset.user_details.password=new_password
            password_reset.user_details.save()
            # password_reset.delete()
            return redirect(DUserLogin)
    return render(request, 'DeliveryBoy/Dreset_password.html', {'token': token})

def DeliveryOrders(request):
    dboy = DeliveryBoy.objects.get(username = request.session['duser'])
    data = ProductsOrders.objects.filter(order_status='ordered').order_by('-created_at')
    return render(request, 'DeliveryBoy/DeliveryOrders.html', {'duser': request.session.get('duser'),'dboy':dboy,'order_details':data})

def AcceptOrder(request,i):
    data = ProductsOrders.objects.get(pk=i)
    dboy = DeliveryBoy.objects.get(username = request.session['duser'])
    if dboy.status == 'approved':
        data.order_status = 'deliveryboyaccepted'
        data.delivery_boy = dboy
        dboy.work_status = 'bussy'
        dboy.save()
        data.save()
        return redirect(DeliveryHistory)
    elif dboy.status == 'rejected':
        messages.error(request,'Your Are Rejected By Admin')
        return redirect(DeliveryOrders)
    else:
        messages.error(request,'Your Are Not Approved By Admin')
        return redirect(DeliveryOrders)


def DeliveryHistory(request):
    dboy = DeliveryBoy.objects.get(username = request.session['duser'])
    data = ProductsOrders.objects.filter(delivery_boy=dboy).order_by('-created_at')
    
    return render(request, 'DeliveryBoy/DHistory.html',{'duser': request.session.get('duser'),'details':data,'current_point':dboy.points,'next':dboy.points-1})
def CancelDeliveryorder(request,i):
    data = ProductsOrders.objects.get(pk=i)
    dboy = DeliveryBoy.objects.get(username = request.session['duser'])
    dboy.points -= 1
    
    if dboy.points == 0:
        dboy.status = 'rejected'
    dboy.save()  
    data.order_status = 'ordered'
    data.delivery_boy = None
    data.save()
    return redirect(DeliveryHistory)

def deliveryotp(request,i):
    dboy = DeliveryBoy.objects.get(username = request.session.get('duser'))
    data = ProductsOrders.objects.get(pk=i)
    if request.method == "POST":
        if data.product_code == request.POST.get('otp'):
            data.order_status = 'delivered'
            dboy.work_status = 'free'
            dboy.save()
            data.save()
        else:
            messages.error(request,'Invalid OTP  ')
    return redirect(DeliveryHistory)


#Admin==============================================================================================================

def AdminLogin(request):
    if request.method == 'POST':
        if request.POST.get('username') == 'Admin' and request.POST.get('password') == 'AutoCarAdmin':
            request.session['admin'] = 'Admin'
            messages.success(request,'Welcome back Admin')
            return redirect(AdminHome)
        else:
            messages.error(request,'invalid Details! Please enter correct Username and  Password')
            return redirect(AdminLogin)
    return render(request,'Admin/AdminLogin.html')

def AdminHome(request):
     data = Products.objects.all()
     count = 0
     for i in data:
        if i.quantity <= 5:
                count +=1
     return render(request,'Admin/AdminHome.html',{'admin': request.session.get('admin'),'count':count})

def countstock():
    data = Products.objects.all()
    count = 0
    for i in data:
        if i.quantity <= 5:
            count +=1
    return count
def AdminViewProducts(request):
    data = Products.objects.all()
    
    return render(request,'Admin/AdminViewProducts.html',{'admin': request.session.get('admin'),'products':data,'count':countstock()})


from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist

def UpdateProduct(request):
    try:
        if request.method == 'POST':
            # Retrieve data from the form
            product_id = request.POST.get('id')
            product_name = request.POST.get('product_name')
            product_details = request.POST.get('product_details')
            product_price = request.POST.get('product_price')
            product_quantity = request.POST.get('quantity')
            product_status = request.POST.get('status')
            product_image = request.FILES.get('product_image')  # Handle the image upload

            # Fetch the product object
            product = Products.objects.get(pk=product_id)

            # Update the product fields
            product.product_name = product_name
            product.product_details = product_details
            product.product_price = product_price
            product.quantity = product_quantity
            product.status = product_status

            # Update the image only if a new file is uploaded
            if product_image:
                product.product_image = product_image

            # Save the changes to the database
            product.save()
            return redirect(AdminViewProducts)  # Replace with the correct redirect view
    except ObjectDoesNotExist:
        print(f"Product with id {product_id} does not exist.")
    except Exception as e:
        print(e)
   


def UpdateImage(request, i):   
    product = Products.objects.get(pk=i)

    if request.method == 'POST':
        form = ProductImageForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect(AdminViewProducts)  # Replace with your actual view name
        else:
            return redirect(AdminViewProducts) 

    # Render the form for GET request
    form = ProductImageForm(instance=product)
    return render(request, 'update_image.html', {'form': form, 'product': product,'count':countstock()})


def DeleteProduct(request):
    if request.method == 'POST':
        product_id = request.POST.get('id')
        product = Products.objects.get(pk=product_id)
        product.delete()
        return redirect(AdminViewProducts)



def AdminAddProducts(request):
    if request.method == 'POST':
        # Create an instance of the form with POST data and files (if any)
        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():
            # Save the form data to create a new product
            form.save()
            # Redirect to a page where the product is listed (e.g., AdminViewProducts)
            return redirect(AdminViewProducts)  # Adjust the redirect path as necessary
    else:
        # Initialize the form if it's a GET request
        form = ProductForm()

    # Render the page with the form
    return render(request, 'Admin/AdminAddProducts.html', {'admin': request.session.get('admin'),'form': form,'count':countstock()})



def AdminViewServices(request):
    data = services.objects.all()
    return render(request, 'Admin/AdminViewServices.html', {'admin': request.session.get('admin'),'services': data,'count':countstock()})





def UpdateService(request):
    try:
        if request.method == 'POST':
            # Retrieve data from the form
            service_id = request.POST.get('id')
            service_name = request.POST.get('service_name')
            service_discription = request.POST.get('service_discription')
            service_amount = request.POST.get('service_amount')
            service_status = request.POST.get('status')
            service_image = request.FILES.get('service_image')  # Handle the image upload

            # Fetch the product object
            service = services.objects.get(pk=service_id)

            # Update the product fields
            service.service_name = service_name
            service.service_discription = service_discription
            service.service_amount = service_amount
            service.status = service_status

            # Update the image only if a new file is uploaded
            if service_image:
                service.service_image = service_image

            # Save the changes to the database
            service.save()

            # Redirect to a success page (replace with the correct view name)
            return redirect(AdminViewServices)

    except ObjectDoesNotExist:
        print(f"Product with id {service_id} does not exist.")
        return HttpResponse("Product not found", status=404)  # Return a 404 if the product is not found
    except Exception as e:
        print(e)
        return HttpResponse(f"An error occurred: {str(e)}", status=500)  # Return a 500 if any other exception occurs


def DeleteService(request):
        if request.method == 'POST':
            service_id = request.POST.get('id')
            service = services.objects.get(pk=service_id)
            service.delete()
            return redirect(AdminViewServices)
        
        


def AdminAddService(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,'Services Add Successfully')
            return redirect(AdminViewServices)  # Adjust the redirect path as necessary
    
    form = ServiceForm()
    print(form.fields)
    print('------------------')

    return render(request, 'Admin/AdminAddServices.html', {'admin': request.session.get('admin'),'form': form,'count':countstock()})

def StockUpdate(request):
    data = Products.objects.all()
    filter =[]
    for i in data:
        if i.quantity <= 5:
            filter.append(i)
    return render(request,'Admin/StockUpdate.html',{'admin': request.session.get('admin'),'products':filter,'s':5,'count':countstock()})
def StockFilter(request):
    if request.method == 'POST':
        data = Products.objects.all()
        filter =[]
        for i in data:
            if i.quantity <= int(request.POST['quantity']):
                filter.append(i)
        return render(request,'Admin/StockUpdate.html',{'admin': request.session.get('admin'),'products':filter,'s':request.POST['quantity'],'count':countstock()})
def ItemUpdate(request,i):
    if request.method == 'POST':
        q = request.POST['quantity']
        data = Products.objects.get(pk=i)
        data.quantity = q
        data.save()
        messages.success(request,'details updated')
        return redirect(StockUpdate)

def ViewUsers(request):
    users = user_details.objects.all()
    return render(request, 'Admin/ViewUsers.html',{'admin': request.session.get('admin'),'users': users,'count':countstock()})

def ViewDeliveryBoys(request):
    approved_dboy = DeliveryBoy.objects.filter(status = 'approved')
    not_approved = DeliveryBoy.objects.filter(status = 'not approved')
    rejected = DeliveryBoy.objects.filter(status ='rejected')
    return render(request, 'Admin/ViewDeliveryBoy.html',{'admin': request.session.get('admin'),'approved_dboy': approved_dboy,'not_approved': not_approved,'rejected': rejected,'count':countstock()})

def DboyStatusUpdate(request):
    if request.method == 'POST':
        deliveryboy_id = request.POST.get("deliveryboy_id")
        new_status = request.POST.get("status")
        data =DeliveryBoy.objects.get(pk = deliveryboy_id )
        data.status = new_status
        data.save()
        return redirect(ViewDeliveryBoys)

def UserDelete(request,i):
    data = user_details.objects.get(pk = i)
    data.delete()
    return redirect(ViewUsers)

def UserStatusUpdate(request):
    if request.method == 'POST':
        user_id = request.POST.get("user_id")
        new_status = request.POST.get("status")
        data =user_details.objects.get(pk = user_id )
        data.status = new_status
        data.save()
        return redirect(ViewUsers)
    
def ViewBookings(request):
    upcomming = BookingOrders.objects.filter(status='Pending').order_by('-created_at')
    cancelled = BookingOrders.objects.filter(status='cancelled').order_by('-created_at')
    c=[]
    for i in cancelled:
        d={
            'pk': i.pk,
            'amount': i.payment_amount * 100
        }
        c.append(d)
    completed = BookingOrders.objects.filter(status = 'completed').order_by('-created_at')      
    return render(request,'Admin/ViewBookings.html',{'admin': request.session.get('admin'),'upcomming':upcomming,'cancelled':cancelled,'completed':completed,'count':countstock(),'amount':c})
def UpdateBookingStatus(request):
     if request.method == 'POST':
        order_id = request.POST.get("order_id")
        print('================================================================')
        print(order_id)
        new_status = request.POST.get("status")
        data =BookingOrders.objects.get(pk = order_id )
        data.status = new_status
        data.save()
        return redirect(ViewBookings)


def RefundPayment(request,i):
    i = float(i)
    i*=100
    print('=================    ====    === ==')
    print(i)    
   
          
        
    
    
    
    order_currency = 'INR'  # noqa: F841
    client = razorpay.Client(
         auth=("rzp_test_SROSnyInFv81S4", "WIWYANkTTLg7iGbFgEbwj4BM"))
    payment = client.order.create({'amount': i* 100, 'currency':'INR', 'payment_capture':'1'})  # noqa: F841
    return render(request,'user/order_product/payment.html',{'admin':request.session['admin'],'price':i * 100,'p':float(i/100)})


def RefundSuccess(request):
    if request.method == 'POST':
        booking_id = request.POST.get('booking_id')
        
        try:
            # Fetch the booking details based on the booking ID
            details = BookingOrders.objects.get(pk=booking_id)
            
            # Update the refund status to 'completed'
            details.refund_status = 'completed'
            details.save()

            # Send an email notification to the user about the refund completion
            user_email = details.user.email
            subject = "Refund Successful"
            message = f"Dear {details.user.name},\n\nYour booking for {details.services} on {details.date} at {details.time_slot} has been refunded successfully.\n\nRefunded Amount : {details.payment_amount}\n\nThank you for choosing our service.\n\nBest Regards,\nYour Service Team"
            from_email = settings.DEFAULT_FROM_EMAIL  # Ensure you have a default from email set up in settings
            
            send_mail(subject, message, from_email, [user_email])

            # Optionally, you can add a message for the admin user
            messages.success(request, f"Refund completed for booking ID {booking_id} and email sent to {user_email}.")
            
        except BookingOrders.DoesNotExist:
            # Handle case when the booking is not found
            messages.error(request, "Booking not found.")
        
    return redirect(ViewBookings)  # Replace 'ViewBookings' with the correct URL name if necessary


def PayPending(request):
    if request.method == 'POST':
        booking_id = request.POST.get('booking_id')
        
        try:
            # Fetch the booking details based on the booking ID
            details = BookingOrders.objects.get(pk=booking_id)
            
            # Update the refund status to 'completed'
            
            details.payment_status = 'completed'
            details.save()
            print('================================================================')
            print(details.refund_status)
            # Send an email notification to the user about the refund completion
            user_email = details.user.email
            subject = "Payment Successful"
            message = f"Dear {details.user.name},\n\nYour booking for {details.services} on {details.date} at {details.time_slot} has been payed successfully.\n\Payment Amount : {details.payment_amount}\n\nThank you for choosing our service.\n\nBest Regards,\nYour Service Team"
            from_email = settings.DEFAULT_FROM_EMAIL  # Ensure you have a default from email set up in settings
            
            send_mail(subject, message, from_email, [user_email])

            # Optionally, you can add a message for the admin user
            messages.success(request, f"Payment completed for booking ID {booking_id} and email sent to {user_email}.")
            
        except BookingOrders.DoesNotExist:
            # Handle case when the booking is not found
            messages.error(request, "Booking not found.")
        
    return redirect(UserBookingListing)

def ProductOrdersView(request):
    ordered = ProductsOrders.objects.filter(order_status='ordered').order_by('-created_at') | ProductsOrders.objects.filter(order_status='deliveryboyaccepted').order_by('-created_at')
    delivered = ProductsOrders.objects.filter(order_status='delivered').order_by('-created_at')
    cancelled = ProductsOrders.objects.filter(order_status='cancelled').order_by('-created_at')
    c=[]
    for i in cancelled:
        d={
            'pk': i.pk,
            'amount': i.payment_amount * 100
        }
        c.append(d)
    return render(request,'Admin/ProductOrders.html',{'admin': request.session.get('admin'),'ordered':ordered,'cancelled':cancelled,'delivered':delivered,'count':countstock(),'amount':c})
   
   
def ProductRefundSuccess(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        
        try:
            # Fetch the booking details based on the booking ID
            details = ProductsOrders.objects.get(pk=order_id)
            
            # Update the refund status to 'completed'
            details.refund_status = 'completed'
            details.save()

            # Send an email notification to the user about the refund completion
            user_email = details.user_details.email
            subject = "Refund Successful"
            message = f"Dear {details.user_details.name},\n\nYour order for {details.product_details.product_name} on {details.product_details.created_at} has been refunded successfully.\n\nRefunded Amount : {details.payment_amount}\n\nThank you for choosing our service.\n\nBest Regards,\nYour Service Team"
            from_email = settings.DEFAULT_FROM_EMAIL  # Ensure you have a default from email set up in settings
            
            send_mail(subject, message, from_email, [user_email])

            # Optionally, you can add a message for the admin user
            messages.success(request, f"Refund completed for booking ID {order_id} and email sent to {user_email}.")
            
        except ProductsOrders.DoesNotExist:
            # Handle case when the booking is not found
            messages.error(request, "Booking not found.")
        
    return redirect(ProductOrdersView)

def AddBooking(request):
    
    datas = services.objects.all()

    # time_slots = list(range(9, 22))  # 9 to 21 inclusive
    context = {
        
        'services': datas,
        'status':17,
        'admin': request.session.get('admin'),
        'count':countstock()
    }
    return render(request, 'Admin/AddBooking.html', context)

def AdminTimeslot(request):
    if request.method == 'POST':
        # Get the selected services as a list of values
        car_number = request.POST.get('car_number')
        email = request.POST.get('email')
        if car_number:
            pattern = r"^[A-Z]{2}\d{2}[A-Z]{1,3}\d{1,4}$"
            if not re.match(pattern, car_number):
                messages.error(request, 'Enter a valid car number')
                return redirect(Userbooking2) 
        
        
        selected_services = request.POST.getlist('services')
        if not selected_services:
            messages.error(request, 'Please select at least one service')
            return redirect(Userbooking2)
        c = len(selected_services)
        price = c * 100
        s = ','.join(selected_services)                                                                             
        print(s)
        
        # Get the other form fields
        service_date_str = request.POST.get('service_date')
        service_date = datetime.strptime(service_date_str, '%Y-%m-%d').date()
        car_model = request.POST.get('car_model')
         
        print(service_date)
        print("Service date:", service_date, "Type:", type(service_date))

        # Logic to check booked time slots for the selected date
        booked_slots = BookingOrders.objects.filter(date=service_date).values_list('time_slot', flat=True)
        print('booked_slots ----------')
        print(booked_slots)

        # Generate all possible time slots (9 AM to 10 PM)
        all_time_slots = [f"{hour:02}:00" for hour in range(9, 22)]

        # Adjust available slots for today's date
        now = datetime.now()
        if service_date == now.date():
            # Exclude past time slots if booking is for today
            current_hour = now.hour
            print(current_hour)
            print('=========')
            current_time_slot = f"{current_hour:02}:00"
            all_time_slots = [slot for slot in all_time_slots if slot > current_time_slot]

        # Filter available time slots by excluding booked slots
        available_time_slots = [slot for slot in all_time_slots if slot not in booked_slots]
        print("Available time slots:", available_time_slots)

        context = {
            'available_time_slots': available_time_slots,
            'selected_services': s.strip(),
            'car_number': car_number,
            'car_model': car_model,
            'service_date': service_date,
            'car_number': car_number,
            'price': price,
            'email': email,
            'status': 50,
            'admin': request.session.get('admin')
        }
        return render(request, 'Admin/AdminTimslot.html',context)
    

import random
import string

def generate_password():
    # Define the character sets
    uppercase = string.ascii_uppercase
    lowercase = string.ascii_lowercase
    digits = string.digits

    # Ensure at least one character from each set
    password = [
        random.choice(uppercase),
        random.choice(lowercase),
        random.choice(digits)
    ]

    # Fill the rest of the password to meet the length requirement (6 characters)
    all_characters = uppercase + lowercase + digits
    while len(password) < 6:
        password.append(random.choice(all_characters))

    # Shuffle the password to ensure randomness
    random.shuffle(password)

    # Join the list into a string and return
    return ''.join(password)

# Generate and print the password
print("Generated password:", generate_password())



def AdminOrder(request):
    if request.method == 'POST':
        
        
        selected_services = request.POST['services']
        print("selected_services ------------")
        print(selected_services)
        car_model = request.POST['car_model']
        car_number = request.POST['car_number']
        email = request.POST['email']
        if car_number:
            pattern = r"^[A-Z]{2}\d{2}[A-Z]{1,3}\d{1,4}$"
            if not re.match(pattern, car_number):
                messages.error(request,'Enter a valid car number')
                return redirect(Userbooking2)   
        date_str = request.POST['date']
        date_obj = datetime.strptime(date_str, "%b. %d, %Y")  # Convert 'Nov. 15, 2024' to a datetime object
        date = date_obj.strftime("%Y-%m-%d")  # Format the date as 'YYYY-MM-DD'

        time_slot = request.POST['timeSlot']
        print("Time slot ------------")
        print(time_slot)
        words = selected_services.split(',')
        word_count = len(words)
        amount = 100 * word_count * 100 * 100 # Convert to paise
        print('amount ------------')
        print(amount)
        price = amount / 10000
        try:
            user_detail = user_details.objects.get(email = request.POST.get('email'))  # noqa: F823
            
            new_booking=BookingOrders.objects.create(user=user_detail,services = selected_services,car_model = car_model,car_number = car_number,date = date,time_slot = time_slot,payment_amount = price)
            booking_id = new_booking.id
            # Store the booking ID in session
            request.session['booking_id'] = booking_id
            print("Booking id  -----------")
            print(request.session['booking_id'])
        except Exception as e:
            print(e)
            password = generate_password()
            user_detail =user_details.objects.create(username = request.POST.get('username'),name = request.POST.get('username'),password = password, email = email)
            new_booking=BookingOrders.objects.create(user=user_detail,services = selected_services,car_model = car_model,car_number = car_number,date = date,time_slot = time_slot,payment_amount = price)
            booking_id = new_booking.id
            # Store the booking ID in session
            request.session['booking_id'] = booking_id
            print("Booking id  -----------")
            print(request.session['booking_id'])
            
        user_email = user_detail.email # Assuming 'user' session contains the user's details
    
        subject = 'Your Appointment is Booked Successfully!'
        message = f"""
        Hello {user_detail.username},

        Your appointment has been successfully booked. Below are the details:
        
        Booking ID: {new_booking.id}
        Service: {new_booking.services}
        Booked Date: {new_booking.date}
        Time: {new_booking.time_slot}
        
        Payment Status: {new_booking.payment_status}
        
        Login Details :
        Username : {user_detail.username}
        Password : {user_detail.password}
        
        Thank you for booking with us!

        Best regards,
        The Booking Team
        """
    
        send_mail(
            subject, 
            message, 
            settings.DEFAULT_FROM_EMAIL,  # From email address
            [user_email],  # To email address
            fail_silently=False,
        )
        messages.success(request, 'booking added successfully')
        return redirect(AddBooking)
    

def AdminPaymentOrderStatus(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        status = request.POST.get('status')
        BookingOrders.objects.filter(pk=order_id).update(payment_status=status)
    return redirect(ViewBookings)

def Ratings(request):
    data = ProductRate.objects.all()
    return render(request,'Admin/Ratings.html',{'admin': request.session.get('admin'),'ratings':data,'count':countstock()})
