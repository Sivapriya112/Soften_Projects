from django.shortcuts import render,redirect
from . models import *
from django.contrib import messages
from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.utils import timezone
from urllib.parse import quote
import razorpay
from django.views.decorators.csrf import csrf_exempt
from datetime import timedelta
import json
from django.http import JsonResponse
# Create your views here.
def index(request):
    preview_workers = worker_profile.objects.filter(
        is_online=True,
        is_verified=True,
        is_terminated=False
    ).select_related('user')[:5]
    worker_count = worker_profile.objects.filter(
        is_online=True,
        is_verified=True,
        is_terminated=False
    ).count()
    total_workers = worker_profile.objects.filter(is_verified=True).count()
    try:
        total_jobs = booking.objects.filter(status='completed').count()
    except Exception:
        total_jobs = 0

    return render(request, 'index.html', {
        'preview_workers': preview_workers,
        'worker_count': worker_count,
        'total_workers': total_workers,
        'total_jobs': total_jobs,
    })

def register(request):
    if request.method=='POST':
        un=request.POST['username']
        mn=request.POST['mobile']
        em=request.POST['email']
        pas=request.POST['password']
        copass=request.POST['repass']
        rle=request.POST['role']
        if user_register.objects.filter(username=un).exists():
            messages.success(request,'Username already exists!')
            return redirect(register)
        else:
            if pas==copass:
                user_register.objects.create(username=un,mobile=mn,email=em,password=pas,role=rle).save()
                return redirect(login)
            else:
                messages.success(request,'Passwords do not match!')
                return redirect(register)
    return render(request,  'register.html')

def login(request):
    if request.method=='POST':
        uname_get=request.POST['username']
        pass_get=request.POST['password']
        try:
            data=user_register.objects.get(username=uname_get)
            if pass_get==data.password:
                if data.role=='user':
                    request.session['user']=uname_get
                    return redirect(user_home)
                else:
                    request.session['worker']=uname_get
                    return redirect(worker_home)
            else:
                messages.success(request,'Incorrect Password!')
                return redirect(login)
        except Exception as e:
            if uname_get=='admin' and pass_get=='1234':
                request.session['admin']=uname_get
                return redirect(admin_home)
            else:
                messages.success(request,'User does not exist!')
                return redirect(login)
    return render(request, 'login.html')

def logout(request):
    if 'user' in request.session or 'worker' in request.session or 'admin' in request.session:
        request.session.flush()
        return redirect(login)



def worker_home(request):
    if 'worker' not in request.session:
        return redirect(login)
    user = user_register.objects.get(username=request.session['worker'])
    worker, created = worker_profile.objects.get_or_create(user=user)
    bookings = booking.objects.filter(worker=worker,is_closed=False).order_by('-created_at')
    return render(request, 'worker_home.html', {
        'user_name': user.username,
        'worker': worker,
        'bookings': bookings
    })


def update_worker_status(request):
    if 'worker' not in request.session:
        return JsonResponse({'error': 'Unauthorized'}, status=401)

    if request.method == "POST":
        data = json.loads(request.body)

        user = user_register.objects.get(username=request.session['worker'])
        worker, _ = worker_profile.objects.get_or_create(user=user)
        if worker.is_terminated:
            return JsonResponse({
                'error': 'Your account is terminated. Please contact customer care.'
            }, status=403)
        worker.skill = data.get('skill')
        worker.is_online = data.get('is_online')
        worker.save()

        return JsonResponse({'status': 'success'})

def update_booking(request, booking_id, action):
    if 'worker' not in request.session:
        return redirect(login)

    worker_user = user_register.objects.get(username=request.session['worker'])
    worker = worker_profile.objects.get(user=worker_user)
    b = booking.objects.get(id=booking_id, worker=worker)
    if action == 'accept':
        b.status = 'accepted'
    elif action == 'reject':
        b.status = 'rejected'

    b.save()
    return redirect(worker_home)

def user_home(request):
    if 'user' not in request.session:
        return redirect(login)
    user = user_register.objects.get(username=request.session['user'])
    workers = worker_profile.objects.filter(is_online=True,is_verified=True,is_terminated=False)

    if request.method == "POST":
        skill = request.POST.get('job_name', '').strip()
        if skill:
            workers = workers.filter(skill=skill)
    return render(request, 'user_home.html', {
        'user': user.username,
        'workers': workers
    })

def worker_detail(request, id):
    worker = worker_profile.objects.get(id=id)
    user = user_register.objects.get(username=request.session['user'])

    # Only fetch active (not closed) bookings
    # If is_closed=True, treat as no active booking → show booking form
    booking_obj = booking.objects.filter(
        user=user,
        worker=worker,
        is_closed=False
    ).order_by('-id').first()

    return render(request, 'worker_detail.html', {
        'worker': worker,
        'booking': booking_obj
    })


def book_worker(request, id):
    if 'user' not in request.session:
        return JsonResponse({'error': 'unauthorized'}, status=401)

    if request.method != "POST":
        return JsonResponse({'error': 'Invalid request'}, status=400)
    data = json.loads(request.body)

    requested_date = data.get('requested_date')
    requested_time = data.get('requested_time')

    if not requested_date or not requested_time:
        return JsonResponse(
            {'error': 'Date and time required'}, status=400
        )

    user = get_object_or_404(
        user_register, username=request.session['user']
    )
    worker = get_object_or_404(worker_profile, id=id)

    #  Prevent duplicate booking for same date & time
    existing = booking.objects.filter(
        user=user,
        worker=worker,
        requested_date=requested_date,
        requested_time=requested_time,
        is_closed=False
    ).first()

    if existing:
        return JsonResponse({'status': existing.status})

    booking_obj = booking.objects.create(
        user=user,
        worker=worker,
        requested_date=requested_date,
        requested_time=requested_time,
        status='pending'
    )

    return JsonResponse({'status': 'pending'})


def booking_detail(request, id):
    b = get_object_or_404(booking, id=id)
    return render(request, "booking_detail.html", {"b": b})




def update_work_status(request, id):
    if 'worker' not in request.session:
        return JsonResponse({'error': 'Unauthorized'}, status=401)

    if request.method != "POST":
        return JsonResponse({'error': 'Invalid request'}, status=400)

    data = json.loads(request.body)
    action = data.get('action')

    b = booking.objects.get(id=id)

    # START WORK
    if action == "start" and b.work_status == "not_started":
        b.work_status = "in_progress"
        b.work_start_time = timezone.now()
        b.save()
        return JsonResponse({'status': 'started'})

    # END WORK
    if action == "end" and b.work_status == "in_progress":
        b.work_status = "completed"
        b.work_end_time = timezone.now()

        duration = b.work_end_time - b.work_start_time
        total_hours = duration.total_seconds() / 3600

        b.total_hours = round(total_hours, 2)

        # 💰 FARE CALCULATION
        if total_hours <= 4:
            fare = 500
        else:
            extra_hours = total_hours - 4
            fare = 500 + (extra_hours * 130)

        b.fare = round(fare, 2)

        b.save()

        return JsonResponse({
            'status': 'completed',
            'total_hours': b.total_hours,
            'fare': b.fare
        })

    return JsonResponse({'error': 'Invalid action'})

def upload_document(request):
    if 'worker' not in request.session:
        return redirect(login)
    worker_user = user_register.objects.get(username=request.session['worker'])
    worker = worker_profile.objects.get(user=worker_user)
    if request.method == "POST":
        worker.document = request.FILES['document']
        worker.save()
    return redirect(worker_home)



def admin_home(request):
    if 'admin' not in request.session:
        return redirect(login)
    else:
        workers=worker_profile.objects.all()
        return render(request, 'admin_home.html', {'workers':workers})

def verify_worker(request,id):
    if 'admin' not in request.session:
        return redirect(login)
    else:
        worker=worker_profile.objects.get(id=id)
        worker.is_verified=True
        worker.save()
        return redirect(admin_home)

def reject_worker(request,id):
    if 'admin' not in request.session:
        return redirect(login)
    else:
        worker=worker_profile.objects.get(id=id)
        worker.is_verified=False
        worker.document=None
        worker.save()
        return redirect(admin_home)

def collect_cash(request, id):
    if 'worker' not in request.session:
        return JsonResponse({'error': 'Unauthorized'}, status=401)

    if request.method != "POST":
        return JsonResponse({'error': 'Invalid request'}, status=400)

    b = get_object_or_404(booking, id=id)

    if b.work_status != "completed":
        return JsonResponse({'error': 'Work not completed'}, status=400)

    b.payment_status = "paid_cash"
    b.is_closed = True
    b.save()

    return JsonResponse({'status': 'closed'})



def payment(request, id):

    if 'user' not in request.session:
        return redirect(login)

    b = get_object_or_404(booking, id=id)

    if b.work_status != "completed" or b.is_closed:
        return redirect(user_home)

    amount = int(b.fare * 100)

    client = razorpay.Client(
        auth=("rzp_test_SROSnyInFv81S4", "WIWYANkTTLg7iGbFgEbwj4BM")
    )

    order = client.order.create({
        "amount": amount,
        "currency": "INR",
        "payment_capture": "1"
    })

    b.razorpay_order_id = order["id"]
    b.save()

    return render(request, "payment.html", {
        "booking": b,
        "amount": amount,
        "order_id": order["id"],
        "razorpay_key": "rzp_test_SROSnyInFv81S4"
    })
@csrf_exempt
def payment_success(request):
    if request.method == "POST":
        razorpay_order_id = request.POST.get("razorpay_order_id")
        b = booking.objects.get(razorpay_order_id=razorpay_order_id)
        b.payment_status = "paid_online"
        b.is_closed = True
        b.save()
        return redirect(f'/worker_detail/{b.worker.id}')

def submit_complaint(request,worker_id):
    if 'user' not in request.session:
        return redirect(login)
    else:
        user=user_register.objects.get(username=request.session['user'])
        worker=worker_profile.objects.get(id=worker_id)
        complaint.objects.create(user=user,worker=worker,message=request.POST['message']).save()
        messages.success(request,"Thank you for your valuable concern. Our team will review it shortly.")
        return redirect(worker_detail,id=worker_id)



def terminate_worker(request,worker_id):
    worker = worker_profile.objects.get(id=worker_id)
    worker.is_active = False
    worker.is_terminated = True
    worker.save()
    message_pass= """You are terminated from EmployIT due to policy violation.
     Please contact the admin team for enquiry."""
    encoded_message = quote(message_pass)
    whatsapp_url = f"https://wa.me/91{worker.user.mobile}?text={encoded_message}"
    messages.success(request, "Worker terminated successfully")
    return redirect(whatsapp_url)


def warn_worker(request, worker_id):
    worker = worker_profile.objects.get(id=worker_id)
    message = """Warning: A complaint has been raised against you.
     Please maintain professional behavior.
      Contact admin for details."""""
    encoded_message = quote(message)
    whatsapp_url = f"https://wa.me/91{worker.user.mobile}?text={encoded_message}"
    return redirect(whatsapp_url)

def complaints(request):
    if 'admin' not in request.session:
        return redirect(login)
    else:
        complaints = (
            complaint.objects
            .values(
                'user__username',
                'worker__id',
                'worker__user__username').annotate(total=Count('id')).order_by('-total'))
        return render(request, 'complaints.html', {'complaints':complaints})

def view_complaints(request, worker_id, username):
    complaints = complaint.objects.filter(
        worker_id=worker_id,
        user__username=username
    )
    return render(request, 'view_complaints.html', {
        'complaints': complaints
    })



def submit_rating(request, id):
    if 'user' not in request.session:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    if request.method == "POST":
        data = json.loads(request.body)
        rating_value = data.get("rating")
        b = booking.objects.get(id=id)
        if b.is_closed and not b.rating:
            b.rating = int(rating_value)
            b.save()
            return JsonResponse({'status': 'success'})
    return JsonResponse({'error': 'Invalid request'}, status=400)

def booking_detail_user(request):
    if 'user' not in request.session:
        return redirect(login)
    user = user_register.objects.get(username=request.session['user'])
    bookings = booking.objects.filter(user=user).order_by('-created_at')
    return render(request, 'booking_detail_user.html', {
        'user': user.username,
        'bookings': bookings,
    })

def booking_detail_worker(request):
    if 'worker' not in request.session:
        return redirect(login)
    worker = worker_profile.objects.get(user__username=request.session['worker'])
    bookings = booking.objects.filter(worker=worker).order_by('-created_at')
    total_earned = sum(b.fare for b in bookings if b.fare and b.is_closed)
    return render(request, 'booking_detail_worker.html', {
        'worker_name': worker.user.username,
        'bookings': bookings,
        'total_earned': total_earned,
    })
def booking_detail_admin(request, worker_id):
    if 'admin' not in request.session:
        return redirect(login)
    worker = worker_profile.objects.get(id=worker_id)
    bookings = booking.objects.filter(worker=worker).order_by('-requested_date')
    total_earned = sum(b.fare for b in bookings if b.fare and b.is_closed)
    return render(request, 'booking_detail_admin.html', {
        'worker': worker,
        'bookings': bookings,
        'total_earned': total_earned,
    })


