from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.contrib.auth.hashers import make_password,check_password
from .forms import *
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.contrib import messages
from django.shortcuts import get_object_or_404
import re
from django.utils import timezone
from datetime import timedelta
import razorpay
from django.db.models import Q, Case, When, IntegerField
from django.utils.timezone import now


# Create your views here.
def index(request):
    return render(request, template_name='index.html')


def about(request):
    return render(request, template_name='about.html')


def contact(request):
    return render(request, template_name='contact.html')


def stories(request):
    data = Stories.objects.all()
    return render(request, template_name='stories.html', context={'data': data})


def service(request):
    dict_eve = {
        'eve': Events.objects.all()
    }
    return render(request, template_name='service.html', context=dict_eve)


def resorts(request):
    data = Resort.objects.all()
    return render(request, template_name='resorts.html', context={'data': data})


def catering(request):
    data = Catering.objects.all()
    return render(request, template_name='catering.html', context={'data': data})

def is_strong_password(password):
    # Password should be at least 8 characters long, contain uppercase, lowercase, numbers, and special characters
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter."
    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter."
    if not re.search(r"\d", password):
        return False, "Password must contain at least one number."
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False, "Password must contain at least one special character."
    return True, ""


def register(request):
    if request.method == 'POST':
        a = request.POST.get('n1')
        b = request.POST.get('n2')
        c = request.POST.get('n3')
        d = request.POST.get('n4')
        e = request.POST.get('n5')
        f = request.POST.get('n6')
        g = request.POST.get('category')

        if not (a and b and c and d and e and f and g):
            messages.error(request, 'All fields are required.')
            return redirect(register)  # Redirect back to registration form

        try:
            # Check if username or email already exists
            if UserRegister.objects.filter(username=a).exists():
                messages.error(request, "Username is already taken.")
                return redirect(register)

            if UserRegister.objects.filter(email=b).exists():
                messages.error(request, "Email is already taken.")
                return redirect(register)

            # Ensure passwords match
            if e != f:
                messages.error(request, "Passwords do not match.")
                return redirect(register)

            # Check password strength
            is_strong, message = is_strong_password(e)
            if not is_strong:
                messages.error(request, message)
                return redirect(register)

            # Hash the password before saving to the database
            hashed_password = make_password(e)

            # Create the user
            user = UserRegister.objects.create(
                username=a,
                email=b,
                phone=c,
                address=d,
                password=hashed_password,
                category=g
            )

            # Success messages based on the user category
            if g == 'user':
                messages.success(request, 'Registration successful! You can now log in.')
            else:
                messages.info(request, 'Registration submitted! Please wait for admin confirmation.')

            return redirect(login)  # Redirect to the login page

        except Exception as ex:
            messages.error(request, f"An error occurred: {str(ex)}")
            return redirect(register)

    return render(request, 'register.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('n1')
        password = request.POST.get('n2')

        try:
            user = UserRegister.objects.get(username=username)
            if user:
                if user.is_confirmed:
                    if check_password(password, user.password):
                        request.session['user'] = username

                        if user.category == 'tailor':
                            return redirect(tailor_home)
                        elif user.category == 'user':
                            return redirect(account)
                        elif user.category == 'entertainer':
                            return redirect(enter_home)
                        elif user.category == 'catering':
                            return redirect(cater_home)
                        else:
                            messages.error(request, "Invalid category. Please contact support.")
                            return redirect(login)  # Redirect to login page
                    else:
                        messages.error(request, "Incorrect password.")
                        return redirect(login)
                else:
                    messages.error(request, "Your account is not yet confirmed by the admin.")
                    return redirect('login')
        except UserRegister.DoesNotExist:
            if username == 'admin' and password == '1234':
                request.session['admin'] = username
                return redirect(ad_account)
            messages.error(request, "Incorrect username or password.")
            return redirect(login)

    return render(request, 'login.html')


def logout(request):
    request.session.flush()
    return redirect(index)


def account(request):
    if 'user' in request.session:
        data = UserRegister.objects.get(username=request.session['user'])
        return render(request, template_name='account.html', context={'data': data})
    else:
        return redirect(login)


def testimonial(request):
    return render(request, template_name='testimonial.html')


def gallery(request):
    data = Gallery.objects.all()
    return render(request, template_name='gallery.html', context={'data': data})


def video_gallery(request):
    videos = Video.objects.all().order_by('-uploaded_at')
    return render(request, 'video_gallery.html', {'videos': videos})


def shorts(request):
    shorts = Shorts.objects.all().order_by('-uploaded_at')
    return render(request, template_name='shorts.html', context={'shorts': shorts})


def corp(request):
    return render(request, template_name='corp.html')


def beach(request):
    return render(request, template_name='beach.html')


def stitching(request):
    data = Tailor.objects.all()
    return render(request, template_name='stitching.html', context={'data': data})


def wed(request):
    data = Planner.objects.all()
    return render(request, template_name='wed.html', context={'data': data})


def parties(request):
    data = Parties.objects.all()
    return render(request, template_name='parties.html', context={'data': data})


def music(request):
    data = Entertainer.objects.all()
    return render(request, template_name='music.html', context={'data': data})


def profile(request):
    if 'user' in request.session:
        data = UserRegister.objects.get(username=request.session['user'])
        return render(request, template_name='profile.html', context={'data': data})
    return redirect(login)


def uabout(request):
    if 'user' in request.session:
        return render(request, template_name='uabout.html')
    return redirect(login)


def ustories(request):
    if 'user' in request.session:
        data = Stories.objects.all()
        return render(request, template_name='ustories.html', context={'data': data})
    return redirect(ustories)


def uservice(request):
    if 'user' in request.session:
        dict_eve = {
            'eve': Events.objects.all()
        }
        return render(request, template_name='uservice.html', context=dict_eve)
    return redirect(login)


def uresorts(request):
    if 'user' in request.session:
        data = Resort.objects.all()
        return render(request, template_name='uresorts.html', context={'data': data})
    return redirect(login)


def utestimonial(request):
    if 'user' in request.session:
        return render(request, template_name='utestimonial.html')
    return redirect(login)


def ugallery(request):
    if 'user' in request.session:
        data = Gallery.objects.all()
        return render(request, template_name='ugallery.html', context={'data': data})
    return redirect(login)


def uvideo(request):
    if 'user' in request.session:
        videos = Video.objects.all().order_by('-uploaded_at')
        return render(request, 'uvideo.html', {'videos': videos})
    return redirect(login)


def ushorts(request):
    if 'user' in request.session:
        shorts = Shorts.objects.all().order_by('-uploaded_at')
        return render(request, template_name='ushorts.html', context={'shorts': shorts})
    return redirect(login)


def ucorp(request):
    if 'user' in request.session:
        return render(request, template_name='ucorp.html')
    return redirect(login)


def ubeach(request):
    if 'user' in request.session:
        return render(request, template_name='ubeach.html')
    return redirect(login)


def ustitching(request):
    if 'user' in request.session:
        data = Tailor.objects.all()
        return render(request, template_name='ustitching.html', context={'data': data})
    return redirect(login)


def ucatering(request):
    if 'user' in request.session:
        data = Catering.objects.all()
        return render(request, template_name='ucatering.html', context={'data': data})
    return redirect(login)


def uwed(request):
    if 'user' in request.session:
        data = Planner.objects.all()
        return render(request, template_name='uwed.html', context={'data': data})
    return redirect(login)


def uparties(request):
    if 'user' in request.session:
        data = Parties.objects.all()
        return render(request, template_name='uparties.html', context={'data': data})
    return redirect(login)


def umusic(request):
    if 'user' in request.session:
        data = Entertainer.objects.all()
        return render(request, template_name='umusic.html', context={'data': data})
    return redirect(login)


def ucontact(request):
    if 'user' in request.session:
        return render(request, template_name='ucontact.html')
    return redirect(login)


def ad_account(request):
    if 'admin' in request.session:
        return render(request, template_name='ad_account.html')
    else:
        return redirect(login)


def ad_profile(request):
    return render(request, template_name='ad_profile.html')


def ad_stories(request):
    if 'admin' in request.session:
        if request.method == 'POST':
            a = request.FILES['image']
            b = request.POST['name']
            c = request.POST['desc']
            Stories.objects.create(image=a, name=b, desc=c).save()
            messages.error(request, "Created")
            return redirect(ad_stories)
        data = Stories.objects.all()
        return render(request, template_name='ad_stories.html', context={'data': data})
    return redirect(login)


def ad_service(request):
    if 'admin' in request.session:
        if request.method == 'POST':
            a = request.FILES['img']
            b = request.POST['name']
            c = request.POST['desc']
            Events.objects.create(img=a, name=b, desc=c).save()
            return HttpResponse('saved')
        data = Events.objects.all()
        return render(request, template_name='ad_service.html', context={'data': data})
    return redirect(ad_service)


def ad_resorts(request):
    if 'admin' in request.session:
        if request.method == 'POST':
            a = request.FILES['image']
            b = request.POST['name']
            Resort.objects.create(image=a, name=b).save()
            return HttpResponse('saved')
        data = Resort.objects.all()
        return render(request, template_name='ad_resorts.html', context={'data': data})
    return redirect(login)


def ad_gallery(request):
    if 'admin' in request.session:
        if request.method == 'POST':
            a = request.FILES['image1']
            b = request.FILES['image2']
            c = request.FILES['image3']
            d = request.FILES['image4']
            e = request.FILES['image5']
            f = request.FILES['image6']
            Gallery.objects.create(image1=a, image2=b, image3=c, image4=d, image5=e, image6=f).save()
            return HttpResponse('saved')
        data = Gallery.objects.all()
        return render(request, template_name='ad_gallery.html', context={'data': data})
    return redirect(login)


def ad_videos(request):
    if request.method == 'POST':
        a = request.POST['title']
        b = request.POST['description']
        c = request.FILES['video_file']
        Video.objects.create(title=a, description=b, video_file=c).save()
        return HttpResponse('saved')
    data = Video.objects.all()
    return render(request, template_name='ad_videos.html', context={'data': data})


def ad_shorts(request):
    if request.method == 'POST':
        a = request.POST['title']
        b = request.POST['description']
        c = request.FILES['video_file']
        Shorts.objects.create(title=a, description=b, video_file=c).save()
        return HttpResponse('saved')
    data = Shorts.objects.all()
    return render(request, template_name='ad_shorts.html', context={'data': data})


def ad_stitching(request):
    if 'admin' in request.session:
        if request.method == 'POST':
            category = request.POST.get('category')
            image = request.FILES.get('image')
            name = request.POST.get('name')
            desc = request.POST.get('desc')
            username_id = request.POST.get('username')

            # Validate if the user exists
            if UserRegister.objects.filter(id=username_id).exists():
                user = UserRegister.objects.get(id=username_id)
                if category == "tailor":
                    Tailor.objects.create(username=user, image=image, name=name, desc=desc).save()
                elif category == "catering":
                    Catering.objects.create(username=user, image=image, name=name, desc=desc).save()
                elif category == "entertainer":
                    Entertainer.objects.create(username=user, image=image, name=name, desc=desc).save()
                return HttpResponse('Saved successfully')
            else:
                return HttpResponse("User does not exist", status=404)

        # Get all data for the template
        data_tailors = Tailor.objects.all()
        data_caterers = Catering.objects.all()
        data_entertainers = Entertainer.objects.all()

        # Get registered users based on their category
        available_tailors = UserRegister.objects.filter(category='tailor').exclude(
            id__in=Tailor.objects.values_list('username_id', flat=True))
        available_caterers = UserRegister.objects.filter(category='catering').exclude(
            id__in=Catering.objects.values_list('username_id', flat=True))
        available_entertainers = UserRegister.objects.filter(category='entertainer').exclude(
            id__in=Entertainer.objects.values_list('username_id', flat=True))

        return render(request, 'ad_stitching.html', {
            'data_tailors': data_tailors,
            'data_caterers': data_caterers,
            'data_entertainers': data_entertainers,
            'available_tailors': available_tailors,
            'available_caterers': available_caterers,
            'available_entertainers': available_entertainers,
        })

    return redirect(login)


def ad_wed(request):
    if 'admin' in request.session:
        if request.method == 'POST':
            a = request.FILES['image']
            b = request.POST['name']
            Planner.objects.create(image=a, name=b).save()
            return HttpResponse('saved')
        data = Planner.objects.all()
        return render(request, template_name='ad_wed.html', context={'data': data})
    return redirect(login)


def ad_parties(request):
    if 'admin' in request.session:
        if request.method == 'POST':
            a = request.FILES['image']
            b = request.POST['name']
            Parties.objects.create(image=a, name=b).save()
            return HttpResponse('saved')
        data = Parties.objects.all()
        return render(request, template_name='ad_parties.html', context={'data': data})
    return redirect(login)


def ad_music(request):
    if 'admin' in request.session:
        if request.method == 'POST':
            a = request.FILES['image']
            b = request.POST['name']
            Entertainer.objects.create(image=a, name=b).save()
            return HttpResponse('saved')
        data = Entertainer.objects.all()
        return render(request, template_name='ad_music.html', context={'data': data})
    return redirect(login)


def ad_bookings(request):
    if 'admin' in request.session:
        query = request.GET.get('q', '')
        status_filter = request.GET.get('status', '')  # Filter by status
        date_filter = request.GET.get('booking_date', '')  # Filter by booking date

        # Retrieve all bookings initially
        data = Booking.objects.all()

        # Filtering based on query
        if query:
            data = data.filter(
                Q(user_details__username__icontains=query) |  # Filter by username
                Q(event__name__icontains=query) |  # Filter by event name
                Q(address__icontains=query) |  # Filter by address
                Q(status__icontains=query)  # Filter by status
            )

        # Filter by status if selected
        if status_filter:
            data = data.filter(status=status_filter)

        # Filter by booking date if selected
        if date_filter:
            today = timezone.now().date()
            if date_filter == 'today':
                data = data.filter(booking_date=today)
            elif date_filter == 'this_week':
                start_of_week = today - timedelta(days=today.weekday())
                end_of_week = start_of_week + timedelta(days=6)
                data = data.filter(booking_date__range=[start_of_week, end_of_week])
            elif date_filter == 'this_month':
                start_of_month = today.replace(day=1)
                next_month = today.replace(month=today.month % 12 + 1, day=1)
                end_of_month = next_month - timedelta(days=1)
                data = data.filter(booking_date__range=[start_of_month, end_of_month])
            elif date_filter == 'this_year':
                start_of_year = today.replace(month=1, day=1)
                end_of_year = today.replace(month=12, day=31)
                data = data.filter(booking_date__range=[start_of_year, end_of_year])

        # Annotate with custom ordering for status
        data = data.annotate(
            custom_order=Case(
                When(status='pending', then=0),
                When(status='confirmed', then=1),
                When(status='completed', then=2),
                When(status='canceled', then=3),
                When(status='paid', then=4),
                When(status='refunded', then=5),
                default=6,
                output_field=IntegerField(),
            )
        ).order_by('custom_order')  # Ensure this comes after filters

        # Render the template with context
        return render(request, 'ad_bookings.html', {
            'data': data,
            'query': query,
            'status_filter': status_filter,
            'date_filter': date_filter,
        })
    return redirect(login)


def user_details(request):
    if 'admin' in request.session:
        query = request.GET.get('q', '')  # Search query
        category_filter = request.GET.get('category', '')  # Category filter

        categories = ['tailor', 'catering', 'entertainer', 'user']
        users_by_category = {}

        for category in categories:
            users = UserRegister.objects.filter(category=category)

            # Apply search filter
            if query:
                users = users.filter(
                    Q(username__icontains=query) |
                    Q(email__icontains=query) |
                    Q(phone__icontains=query)
                )

            # Apply category filter
            if category_filter and category_filter != category:
                users = []  # Empty the list if it doesn't match the filter

            # Assign filtered users to the dictionary
            users_by_category[category] = users

        return render(request, 'user_details.html', {
            'users_by_category': users_by_category,
            'query': query,
            'category_filter': category_filter,
            'categories': categories,
        })

    return redirect('login')  # Replace 'login' with your actual login view name


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = UserRegister.objects.get(email=email)
        except:
            messages.info(request, "Email id not registered")
            return redirect(forgot_password)
        # Generate and save a unique token
        token = get_random_string(length=4)
        PasswordReset.objects.create(user=user, token=token)

        # Send email with reset link
        reset_link = f'http://127.0.0.1:7000/reset/{token}'
        try:
            send_mail('Reset Your Password', f'Click the link to reset your password: {reset_link}',
                      'settings.EMAIL_HOST_USER', [email], fail_silently=False)
            # return render(request, 'emailsent.html')
        except:
            messages.info(request, "Network connection failed")
            return redirect(forgot_password)

    return render(request, 'forgot.html')


def reset_password(request, token):
    # Verify token and reset the password
    print(token)
    password_reset = PasswordReset.objects.get(token=token)

    # usr = User.objects.get(id=password_reset.user_id)
    if request.method == 'POST':
        new_password = request.POST.get('newpassword')
        hashed_password = make_password(new_password)
        repeat_password = request.POST.get('cpassword')
        if repeat_password == new_password:
            password_reset.user.password = hashed_password
            password_reset.user.save()
            return redirect(login)
    return render(request, 'reset_password.html', {'token': token})


# tailor session
def tailor_home(request):
    if 'user' in request.session:
        data = UserRegister.objects.get(username=request.session['user'])
        return render(request, template_name='tailor_home.html', context={'data': data})
    else:
        return redirect(login)


def tailor_booking(request):
    if 'user' in request.session:
        try:
            user = UserRegister.objects.get(username=request.session['user'])

            if user.category == 'tailor':
                tailor = Tailor.objects.get(username=user)

                bookings = AdminBooking.objects.filter(tailor=tailor).annotate(
                    status_order=Case(
                        When(status='pending', then=0),
                        When(status='confirmed', then=1),
                        When(status='completed', then=2),
                        When(status='canceled', then=3),
                        default=4,
                        output_field=IntegerField()
                    )
                ).order_by('status_order')

                return render(request, 'tailor_booking.html', {'bookings': bookings})
            else:
                return redirect('not_authorized')
        except UserRegister.DoesNotExist:
            return redirect('login')
        except Tailor.DoesNotExist:
            return redirect('not_authorized')
    else:
        return redirect('login')


def tailor_confirm(request, booking_id):
    if 'user' in request.session:
        try:
            # Get the booking
            booking = get_object_or_404(AdminBooking, id=booking_id)

            # Ensure the logged-in tailor is associated with the booking
            user_details = UserRegister.objects.get(username=request.session['user'])
            if booking.tailor and booking.tailor.username == user_details:
                # Update the booking status
                booking.tailor_status = 'confirmed'
                booking.save()
                messages.success(request, "Booking confirmed successfully.")
            else:
                messages.error(request, "You are not authorized to confirm this booking.")
        except UserRegister.DoesNotExist:
            messages.error(request, "User not found.")
    return redirect(tailor_booking)  # Redirect to tailor bookings page


def tailor_ignore(request, booking_id):
    if 'user' in request.session:
        try:
            # Get the booking
            booking = get_object_or_404(AdminBooking, id=booking_id)

            # Ensure the logged-in tailor is associated with the booking
            user_details = UserRegister.objects.get(username=request.session['user'])
            if booking.tailor and booking.tailor.username == user_details:
                # Update the booking status
                booking.tailor_status = 'cancelled'
                booking.save()
                messages.success(request, "Booking ignored successfully.")
            else:
                messages.error(request, "You are not authorized to ignore this booking.")
        except UserRegister.DoesNotExist:
            messages.error(request, "User not found.")
    return redirect(tailor_booking)  # Redirect to tailor bookings page


def tailor_complete(request, booking_id):
    if 'user' in request.session:
        try:
            # Get the booking
            booking = get_object_or_404(AdminBooking, id=booking_id)

            # Ensure the logged-in tailor is associated with the booking
            user_details = UserRegister.objects.get(username=request.session['user'])
            if booking.tailor and booking.tailor.username == user_details:
                # Update the booking status to completed
                booking.tailor_status = 'completed'
                booking.save()
                messages.success(request, "Booking marked as completed.")
            else:
                messages.error(request, "You are not authorized to complete this booking.")
        except UserRegister.DoesNotExist:
            messages.error(request, "User not found.")
    return redirect(tailor_booking)  # Redirect to tailor bookings page


def tailor_profile(request):
    if 'user' in request.session:
        data = UserRegister.objects.get(username=request.session['user'])
        return render(request, template_name='tailor_profile.html', context={'data': data})
    return redirect(login)


# catering session

def cater_home(request):
    if 'user' in request.session:
        data = UserRegister.objects.get(username=request.session['user'])
        return render(request, template_name='cater_home.html', context={'data': data})
    else:
        return redirect(login)


def cater_booking(request):
    if 'user' in request.session:
        try:
            user = UserRegister.objects.get(username=request.session['user'])
            if user.category == 'catering':
                catering = Catering.objects.get(username=user)
                bookings = AdminBooking.objects.filter(catering=catering).annotate(
                    status_order=Case(
                        When(status='pending', then=0),
                        When(status='confirmed', then=1),
                        When(status='completed', then=2),
                        When(status='canceled', then=3),
                        default=4,
                        output_field=IntegerField()
                    )
                ).order_by('status_order')

                return render(request, 'cater_booking.html', {'bookings': bookings})
            else:
                return redirect('not_authorized')
        except (UserRegister.DoesNotExist, Catering.DoesNotExist):
            return redirect('login')
    return redirect('login')


def cater_confirm(request, booking_id):
    if 'user' in request.session:
        try:
            booking = get_object_or_404(AdminBooking, id=booking_id)
            user = UserRegister.objects.get(username=request.session['user'])
            if booking.catering and booking.catering.username == user:
                booking.caterer_status = 'confirmed'
                booking.save()
                messages.success(request, "Booking confirmed successfully.")
            else:
                messages.error(request, "You are not authorized to confirm this booking.")
        except UserRegister.DoesNotExist:
            messages.error(request, "User not found.")
    return redirect(cater_booking)


def cater_ignore(request, booking_id):
    if 'user' in request.session:
        try:
            booking = get_object_or_404(AdminBooking, id=booking_id)
            user = UserRegister.objects.get(username=request.session['user'])
            if booking.catering and booking.catering.username == user:
                booking.caterer_status = 'cancelled'
                booking.save()
                messages.success(request, "Booking ignored successfully.")
            else:
                messages.error(request, "You are not authorized to ignore this booking.")
        except UserRegister.DoesNotExist:
            messages.error(request, "User not found.")
    return redirect(cater_booking)


def cater_complete(request, booking_id):
    if 'user' in request.session:
        try:
            booking = get_object_or_404(AdminBooking, id=booking_id)
            user = UserRegister.objects.get(username=request.session['user'])
            if booking.catering and booking.catering.username == user:
                booking.caterer_status = 'completed'
                booking.save()
                messages.success(request, "Booking marked as completed.")
            else:
                messages.error(request, "You are not authorized to complete this booking.")
        except UserRegister.DoesNotExist:
            messages.error(request, "User not found.")
    return redirect(cater_booking)


def cater_profile(request):
    if 'user' in request.session:
        data = UserRegister.objects.get(username=request.session['user'])
        return render(request, template_name='cater_profile.html', context={'data': data})
    return redirect(login)


# entertaining session
def enter_home(request):
    if 'user' in request.session:
        data = UserRegister.objects.get(username=request.session['user'])
        return render(request, template_name='enter_home.html', context={'data': data})
    else:
        return redirect(login)


def entertainer_booking(request):
    if 'user' in request.session:
        try:
            user = UserRegister.objects.get(username=request.session['user'])
            if user.category == 'entertainer':
                entertainer = Entertainer.objects.get(username=user)
                bookings = AdminBooking.objects.filter(entertainer=entertainer).annotate(
                    status_order=Case(
                        When(status='pending', then=0),
                        When(status='confirmed', then=1),
                        When(status='completed', then=2),
                        When(status='canceled', then=3),
                        default=4,
                        output_field=IntegerField()
                    )
                ).order_by('status_order')
                return render(request, 'entertainer_booking.html', {'bookings': bookings})
            else:
                return redirect('not_authorized')
        except (UserRegister.DoesNotExist, Entertainer.DoesNotExist):
            return redirect('login')
    return redirect('login')


def enter_confirm(request, booking_id):
    if 'user' in request.session:
        try:
            booking = get_object_or_404(AdminBooking, id=booking_id)
            user = UserRegister.objects.get(username=request.session['user'])
            if booking.entertainer and booking.entertainer.username == user:
                booking.entertainer_status = 'confirmed'
                booking.save()
                messages.success(request, "Booking confirmed successfully.")
            else:
                messages.error(request, "You are not authorized to confirm this booking.")
        except UserRegister.DoesNotExist:
            messages.error(request, "User not found.")
    return redirect(entertainer_booking)


def enter_ignore(request, booking_id):
    if 'user' in request.session:
        try:
            booking = get_object_or_404(AdminBooking, id=booking_id)
            user = UserRegister.objects.get(username=request.session['user'])
            if booking.entertainer and booking.entertainer.username == user:
                booking.entertainer_status = 'cancelled'
                booking.save()
                messages.success(request, "Booking ignored successfully.")
            else:
                messages.error(request, "You are not authorized to ignore this booking.")
        except UserRegister.DoesNotExist:
            messages.error(request, "User not found.")
    return redirect(entertainer_booking)


def enter_complete(request, booking_id):
    if 'user' in request.session:
        try:
            booking = get_object_or_404(AdminBooking, id=booking_id)
            user = UserRegister.objects.get(username=request.session['user'])
            if booking.entertainer and booking.entertainer.username == user:
                booking.entertainer_status = 'completed'
                booking.save()
                messages.success(request, "Booking marked as completed.")
            else:
                messages.error(request, "You are not authorized to complete this booking.")
        except UserRegister.DoesNotExist:
            messages.error(request, "User not found.")
    return redirect(entertainer_booking)


def enter_profile(request):
    if 'user' in request.session:
        data = UserRegister.objects.get(username=request.session['user'])
        return render(request, template_name='enter_profile.html', context={'data': data})
    else:
        return redirect(login)


def resort_delete(request, d):
    if 'admin' in request.session:
        data = Resort.objects.get(pk=d)
        print(data)
        data.delete()
        return redirect(ad_resorts)
    return redirect(login)


def planner_delete(request, d):
    if 'admin' in request.session:
        data = Planner.objects.get(pk=d)
        print(data)
        data.delete()
        return redirect(ad_wed)
    return redirect(login)


def parties_delete(request, d):
    if 'admin' in request.session:
        data = Parties.objects.get(pk=d)
        print(data)
        data.delete()
        return redirect(ad_parties)
    return redirect(login)


def music_delete(request, d):
    if 'admin' in request.session:
        data = Entertainer.objects.get(pk=d)
        print(data)
        data.delete()
        return redirect(ad_music)
    return redirect(login)


def stories_delete(request, d):
    if 'admin' in request.session:
        data = Stories.objects.get(pk=d)
        print(data)
        data.delete()
        return redirect(ad_stories)
    return redirect(login)


def tailor_delete(request, d):
    if 'admin' in request.session:
        data = Tailor.objects.get(pk=d)
        print(data)
        data.delete()
        return redirect(ad_stitching)
    return redirect(login)


def user_confirm(request, d):
    if 'admin' in request.session:
        user = get_object_or_404(UserRegister, pk=d)
        user.is_confirmed = True  # Update the confirmation status
        user.save()
        return redirect(user_details)  # Redirect to user details page
    return redirect(login)


def user_delete(request, d):
    if 'admin' in request.session:
        data = UserRegister.objects.get(pk=d)
        print(data)
        data.delete()
        return redirect(user_details)
    return redirect(login)


def resort_update(request, d):
    if 'admin' in request.session:
        data = Resort.objects.get(pk=d)
        print(data)
        if request.method == 'POST':
            a = request.FILES['image']
            b = request.POST['name']
            Resort.objects.filter(pk=d).update(image=a, name=b)
            return redirect(ad_resorts)
        return render(request, template_name='update.html', context={'data': data})
    return redirect(login)


def video_update(request, d):
    if 'admin' in request.session:
        try:
            video = Video.objects.get(pk=d)
        except Shorts.DoesNotExist:
            return redirect(ad_videos)  # Handle case where Shorts does not exist

        if request.method == 'POST':
            a = request.POST.get('title', video.title)  # Use existing value if not provided
            b = request.POST.get('description', video.description)

            if 'video_file' in request.FILES:  # Check if a new video file is uploaded
                c = request.FILES['video_file']
                video.video_file = c  # Update the video_file field

            # Update other fields
            video.title = a
            video.description = b
            video.save()  # Save the updated object

            return redirect(ad_videos)

        return render(request, 'update.html', {'video': video})
    return redirect(login)


def video_delete(request, d):
    if 'admin' in request.session:
        data = Video.objects.get(pk=d)
        print(data)
        data.delete()
        return redirect(ad_videos)
    return redirect(login)


def shorts_update(request, d):
    if 'admin' in request.session:
        try:
            shorts = Shorts.objects.get(pk=d)
        except Shorts.DoesNotExist:
            return redirect(ad_shorts)  # Handle case where Shorts does not exist

        if request.method == 'POST':
            a = request.POST.get('title', shorts.title)  # Use existing value if not provided
            b = request.POST.get('description', shorts.description)

            if 'video_file' in request.FILES:  # Check if a new video file is uploaded
                c = request.FILES['video_file']
                shorts.video_file = c  # Update the video_file field

            # Update other fields
            shorts.title = a
            shorts.description = b
            shorts.save()  # Save the updated object

            return redirect(ad_shorts)

        return render(request, 'update.html', {'shorts': shorts})
    return redirect(login)


def shorts_delete(request, d):
    if 'admin' in request.session:
        shorts = Shorts.objects.get(pk=d)
        print(shorts)
        shorts.delete()
        return redirect(ad_shorts)
    return redirect(login)


def gallery_update(request, d):
    if 'admin' in request.session:
        data = Gallery.objects.get(pk=d)
        print(data)

        if request.method == 'POST':
            a = request.FILES['image1']
            b = request.FILES['image2']
            c = request.FILES['image3']
            e = request.FILES['image4']
            d = request.FILES['image5']
            f = request.FILES['image6']

            data.image1 = a
            data.image2 = b
            data.image3 = c
            data.image4 = d
            data.image5 = e
            data.image6 = f
            data.save()

            return redirect(ad_gallery)
        return render(request, template_name='update.html', context={'data': data})
    return redirect(login)


def galley_delete(request, d):
    if 'admin' in request.session:
        data = Gallery.objects.get(pk=d)
        print(data)
        data.delete()
        return redirect(ad_gallery)
    return redirect(login)


def admin_booking(request):
    if 'admin' in request.session:
        query = request.GET.get('q', '')
        status_filter = request.GET.get('status', '')  # Filter by status
        date_filter = request.GET.get('booking_date', '')  # Filter by booking date
        tailors = Tailor.objects.all()  # Get all available tailors
        caterers = Catering.objects.all()  # Get all available caterers
        entertainers = Entertainer.objects.all()  # Get all available entertainers

        if request.method == "POST":
            form = AdminBookingForm(request.POST)
            if form.is_valid():
                booking = form.save(commit=False)
                booking.user = request.user
                booking.save()
                messages.success(request, "Booking created successfully!")
                return redirect(admin_booking)
            else:
                messages.error(request, "Please correct the errors below.")
        else:
            form = AdminBookingForm()
            data = AdminBooking.objects.all()

            # Filter by search query
            if query:
                data = data.filter(
                    Q(booking__user_details__username__icontains=query) |
                    Q(booking__event__name__icontains=query) |
                    Q(booking__address__icontains=query) |
                    Q(status__icontains=query)
                )

            # Filter by status if selected
            if status_filter:
                data = data.filter(status=status_filter)

            # Filter by booking date if selected
            if date_filter:
                today = now().date()
                if date_filter == 'today':
                    data = data.filter(booking__booking_date=today)
                elif date_filter == 'this_week':
                    start_of_week = today - timedelta(days=today.weekday())
                    end_of_week = start_of_week + timedelta(days=6)
                    data = data.filter(booking__booking_date__range=[start_of_week, end_of_week])
                elif date_filter == 'this_month':
                    start_of_month = today.replace(day=1)
                    next_month = today.replace(month=today.month % 12 + 1, day=1)
                    end_of_month = next_month - timedelta(days=1)
                    data = data.filter(booking__booking_date__range=[start_of_month, end_of_month])
                elif date_filter == 'this_year':
                    start_of_year = today.replace(month=1, day=1)
                    end_of_year = today.replace(month=12, day=31)
                    data = data.filter(booking__booking_date__range=[start_of_year, end_of_year])

            # Update the status dynamically
            for booking in data:
                # Default unselected services to 'nil'
                booking.tailor_status = booking.tailor_status or 'nil'
                booking.caterer_status = booking.caterer_status or 'nil'
                booking.entertainer_status = booking.entertainer_status or 'nil'

                # Calculate overall booking status based on service statuses
                statuses = [
                    booking.tailor_status,
                    booking.caterer_status,
                    booking.entertainer_status,
                ]
                statuses = [status for status in statuses if
                            status not in ['nil', None]]  # Exclude 'nil' or empty statuses

                if "cancelled" in statuses:
                    booking.status = "cancelled"
                elif "pending" in statuses:
                    booking.status = "pending"
                elif all(status == "confirmed" for status in statuses):
                    booking.status = "confirmed"
                elif all(status == "completed" for status in statuses):
                    booking.status = "completed"
                else:
                    booking.status = "in_progress"  # Default fallback status

                booking.save()
            # Annotate and order data for display
            data = data.annotate(
                custom_order=Case(
                    When(status="cancelled", then=0),
                    When(status="pending", then=1),
                    When(status="confirmed", then=2),
                    When(status="completed", then=3),
                    default=4,
                    output_field=IntegerField(),
                )
            ).order_by("custom_order")

            return render(request, 'admin_booking.html', {
                'form': form,
                'data': data,
                'query': query,
                'status_filter': status_filter,
                'date_filter': date_filter,
                'tailors': tailors,
                'caterers': caterers,
                'entertainers': entertainers,
            })

    return redirect(login)


def cancel_admin_booking(request, booking_id):
    if 'admin' in request.session:
        booking = get_object_or_404(AdminBooking, id=booking_id)
        booking.status = 'canceled'
        booking.save()
        messages.warning(request, f"Booking for {booking.username} has been cancelled.")
        return redirect(admin_booking)
    return redirect(login)


def booking(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            total_payment = str(Booking.total_payment)
            advance_payment = form.cleaned_data.get('advance_payment', 0)

            if advance_payment < 5000:
                messages.warning(request, "Advance amount must be 5000 or higher.")
                return redirect(Booking)

            booking_data = {
                'phone': form.cleaned_data['phone'],
                'event_id': form.cleaned_data['event'].id,  # Assuming the form has an 'event' field
                'address': form.cleaned_data['address'],
                'booking_date': str(form.cleaned_data['booking_date']),  # Convert to string for session storage
                'advance_payment': float(advance_payment),
                'total_payment': total_payment,
            }
            request.session['booking_data'] = booking_data
            return redirect(payment)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = BookingForm()
        user = UserRegister.objects.get(username=request.session['user'])
        data = Booking.objects.filter(user_details=user).order_by('-booked_on')

        for booking in data:
            if booking.total_payment is not None and booking.advance_payment is not None:
                booking.balance_payment = booking.total_payment - booking.advance_payment
            else:
                booking.balance_payment = None

        return render(request, 'booking.html', {'form': form, 'data': data})
    return redirect(login)


def payment(request):
    booking_data = request.session.get('booking_data')
    if not booking_data:
        messages.error(request, "Session expired. Please try booking again.")
        return redirect(booking)

    advance_payment = int(float(booking_data['advance_payment']) * 100)
    client = razorpay.Client(auth=("rzp_test_SROSnyInFv81S4", "WIWYANkTTLg7iGbFgEbwj4BM"))

    payment_order = client.order.create({
        'amount': advance_payment,
        'currency': 'INR',
        'payment_capture': '1'
    })

    request.session['payment_order_id'] = payment_order['id']  # Store the order ID for later verification
    return render(request, "payment.html", context={'amount': advance_payment})


def success(request):
    if 'user' not in request.session or 'booking_data' not in request.session:
        messages.error(request, "Unauthorized access or session expired.")
        return redirect('booking')  # Redirect to booking page if session data is missing

    # Retrieve user and booking data from session
    user = UserRegister.objects.get(username=request.session['user'])
    booking_data = request.session.pop('booking_data')  # Remove booking data from session after use

    # Save the booking to the database
    booking = Booking(
        user_details=user,
        phone=booking_data['phone'],
        event=Events.objects.get(id=booking_data['event_id']),
        address=booking_data['address'],
        booking_date=booking_data['booking_date'],
        advance_payment=str(booking_data['advance_payment']),
        status='pending',  # Mark the booking as confirmed
    )
    booking.save()

    # Render the success page with booking details
    return render(request, 'success.html', {'booking': booking})


def confirm_booking(request, booking_id):
    if 'admin' in request.session:
        booking = get_object_or_404(Booking, id=booking_id)
        booking.status = 'confirmed'
        booking.save()  # Save the updated status
        messages.success(request, f"Booking ID {booking.id} has been confirmed.")
        return redirect(ad_bookings)  # Redirect to admin bookings
    return redirect(login)  # Redirect to login if not logged in


def cancel_booking(request, booking_id):
    if 'admin' in request.session:
        booking = get_object_or_404(Booking, id=booking_id)

        if booking.advance_payment > 0:
            # Redirect to refund processing
            return redirect('refund_payment', booking_id=booking.id)

        # If no advance payment, directly mark as canceled
        booking.status = 'canceled'
        booking.refund_processed = False  # No refund required
        booking.save()

        messages.warning(request, f"Booking ID {booking.id} has been cancelled without a refund.")
        return redirect(ad_bookings)
    return redirect(login)


def booking_cancel(request, booking_id):
    if 'user' in request.session:  # Ensure the user is logged in
        booking = get_object_or_404(Booking, id=booking_id)

        # Update booking status to "canceled"
        booking.status = 'canceled'
        booking.refund_processed = True  # Optional: Handle refund logic here
        booking.save()

        messages.warning(request, f"Booking ID {booking.id} has been cancelled, and the refund has been processed.")
        return redirect('booking')  # Redirect to the booking page
    return redirect('login')


def completed_booking(request, booking_id):
    if 'admin' in request.session:
        booking = get_object_or_404(Booking, id=booking_id)
        booking.status = 'completed'
        booking.save()
        messages.success(request, f"Booking ID {booking.id} has been marked as completed.")
        return redirect(ad_bookings)
    return redirect(login)


def paid_booking(request, booking_id):
    if 'admin' in request.session:
        booking = get_object_or_404(Booking, id=booking_id)
        booking.status = 'paid'
        booking.save()
        messages.success(request, f"Booking ID {booking.id} has been marked as paid.")
        return redirect(ad_bookings)
    return redirect(login)  # Redirect to the bookings page after marking as paid


def update_total_payment(request, booking_id):
    if request.method == 'POST':
        booking = get_object_or_404(Booking, id=booking_id)
        total_payment = request.POST.get('total_payment')
        booking.total_payment = total_payment  # Update the total payment field
        booking.total_payment_updated = True  # Mark the update
        booking.save()
    return redirect(ad_bookings)  # Redirect to the bookings page after updating the payment


def refund_payment(request, booking_id):
    if 'admin' in request.session:
        booking = get_object_or_404(Booking, id=booking_id)

        # Calculate the refund amount
        refund_amount = int(booking.advance_payment * 100)  # Convert to paise

        client = razorpay.Client(auth=("rzp_test_SROSnyInFv81S4", "WIWYANkTTLg7iGbFgEbwj4BM"))

        # Create a payment for refund
        payment_order = client.order.create({
            'amount': refund_amount,
            'currency': 'INR',
            'payment_capture': '1'
        })

        # Store payment details in session
        request.session['refund_booking_id'] = booking_id
        request.session['refund_order_id'] = payment_order['id']
        request.session['refund_payment_id'] = payment_order['id']  # Store payment_id here

        return render(request, "refund_payment.html", {
            'amount': refund_amount,
            'payment_id': payment_order['id'],
            'booking_id': booking_id
        })
    return redirect(login)


def refund_success(request):
    # Ensure the user is logged in as admin
    if 'admin' not in request.session:
        messages.error(request, "Unauthorized access.")
        return redirect(login)

    # Retrieve refund details from session
    booking_id = request.session.get('refund_booking_id')
    payment_id = request.session.get('refund_payment_id')  # Fetch payment_id from session

    if not booking_id or not payment_id:
        messages.error(request, "Invalid session or refund process. Please try again.")
        return redirect(ad_bookings)

    booking = get_object_or_404(Booking, id=booking_id)
    booking.status = 'refunded'  # Ensure the status is exactly 'Refunded'
    booking.save()

    # Clear session variables for the refund process
    request.session.pop('refund_booking_id', None)
    request.session.pop('refund_order_id', None)
    request.session.pop('refund_payment_id', None)

    # Notify admin
    messages.success(request, f"Booking ID {booking.id} has been successfully refunded.")
    return render(request, 'refund_success.html', {'booking': booking})


def terms(request):
    return render(request, template_name='terms.html')


def uterms(request):
    if 'user' in request.session:
        return render(request, template_name='uterms.html')
    return redirect(login)


def change_tailor(request, booking_id):
    booking = get_object_or_404(AdminBooking, pk=booking_id)

    if request.method == 'POST':
        tailor_id = request.POST.get('tailor')
        if tailor_id:
            tailor = get_object_or_404(Tailor, pk=tailor_id)
            booking.tailor = tailor
            booking.tailor_status = 'pending'  # Set status to confirmed for the new tailor
            booking.save()
        else:
            booking.tailor = None  # If no tailor selected, set to None
            booking.tailor_status = 'nil'  # Set status to 'nil'
            booking.save()

    return redirect(admin_booking)  # Redirect to the booking page


# View to change the caterer
def change_caterer(request, booking_id):
    booking = get_object_or_404(AdminBooking, pk=booking_id)

    if request.method == 'POST':
        caterer_id = request.POST.get('caterer')
        if caterer_id:
            caterer = get_object_or_404(Catering, pk=caterer_id)
            booking.catering = caterer
            booking.caterer_status = 'pending'  # Set status to confirmed for the new caterer
            booking.save()
        else:
            booking.catering = None  # If no caterer selected, set to None
            booking.caterer_status = 'nil'  # Set status to 'nil'
            booking.save()

    return redirect(admin_booking)  # Redirect to the booking page


# View to change the entertainer
def change_entertainer(request, booking_id):
    booking = get_object_or_404(AdminBooking, pk=booking_id)

    if request.method == 'POST':
        entertainer_id = request.POST.get('entertainer')
        if entertainer_id:
            entertainer = get_object_or_404(Entertainer, pk=entertainer_id)
            booking.entertainer = entertainer
            booking.entertainer_status = 'pending'  # Set status to confirmed for the new entertainer
            booking.save()
        else:
            booking.entertainer = None  # If no entertainer selected, set to None
            booking.entertainer_status = 'nil'  # Set status to 'nil'
            booking.save()

    return redirect(admin_booking)  # Redirect to the booking page