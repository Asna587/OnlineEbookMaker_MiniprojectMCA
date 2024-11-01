from django.core.files.storage import FileSystemStorage
from django.shortcuts import render,redirect,HttpResponse
from .models import *
from django.core.paginator import Paginator
from django.utils import timezone
from django.views.decorators.http import require_POST


def logout(request):
    del request.session['lid']
    return redirect('/')

def home(request):
    return render(request, 'Store/home.html')

def login(request):
    return render(request, 'Store/login.html')

def login_post(request):
    username = request.POST['username']
    password = request.POST['password']

    login_fetch = Login.objects.filter(username=username,password=password)
    if login_fetch.exists():
        login_get = Login.objects.get(username=username,password=password)
        request.session['lid'] = login_get.id
        if login_get.type == 'admin':
            return redirect('/admin_home')
        elif login_get.type == 'user':
            user = User.objects.get(LOGIN_id=request.session['lid'])
            request.session['user_name'] = user.name
            return redirect('/user_home')
        else:
            return HttpResponse('''<script>alert("Credentials Mismatches"); window.location='/';</script>''')
    else:
        return HttpResponse('''<script>alert("Invalid"); window.location='/';</script>''')

def user_registration(request):
    if request.method == 'POST':
        name=request.POST['name']
        dob=request.POST['dob']
        phone=request.POST['phone']
        email=request.POST['email']
        photo=request.FILES['photo']
        place=request.POST['place']
        pin=request.POST['pin']
        post=request.POST['post']
        gender=request.POST['gender']
        password=request.POST['password']

        fs = FileSystemStorage()
        fp = fs.save(photo.name,photo)

        login_details = Login(username=email,password=password,type='user')
        login_details.save()

        profile = User(LOGIN=login_details,name=name,dob=dob,phone=phone,email=email,photo=fp,place=place,pin=pin,post=post,gender=gender)
        profile.save()
        return HttpResponse('''<script>alert("Registration Successfully Completed"); window.location='/';</script>''')
    return render(request, 'User/registration.html')


def admin_home(request):
    return render(request, 'Admin/admin_home.html')


def user_home(request):
    return render(request, 'User/user_home.html')

def manage_book(request):
    books = Book.objects.filter(USER__LOGIN=request.session['lid'])
    return render(request, 'User/view_my_books.html',{'books':books})

def add_new_book(request):
    if request.method == 'POST':
        book_name=request.POST['book_name']
        description=request.POST['description']
        file=request.FILES['file']
        thumbnail=request.FILES['thumbnail']

        fs = FileSystemStorage()
        fp = fs.save(file.name,file)

        new_book = Book(
            USER=User.objects.get(LOGIN_id=request.session['lid']),
            book_name=book_name,
            thumbnail=thumbnail,
            description=description,
            file=fp
        )
        new_book.save()
        return HttpResponse('''<script>alert("Book Successfully Added"); window.location='/manage_book';</script>''')
    return render(request,'User/add_new_book.html')

def edit_book(request,id):
    book = Book.objects.get(id=id)
    if request.method == 'POST':
        book.book_name=request.POST['book_name']
        book.description=request.POST['description']
        if 'thumbnail' in request.FILES:
            book.thumbnail=request.FILES['thumbnail']
            book.save()
        if 'file' in request.FILES:
            book.file=request.FILES['file']
            book.save()
        book.save()
        return HttpResponse('''<script>alert("Book Successfully Edited"); window.location='/manage_book';</script>''')
    return render(request, 'User/edit_book.html',{'book':book})

def delete_book(request,id):
    book = Book.objects.get(id=id)
    book.delete()
    return HttpResponse('''<script>alert("Book Successfully Deleted"); window.location='/manage_book';</script>''')

def view_published_books(request):
    books = Book.objects.all().order_by('-id')
    paginator = Paginator(books, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'User/view_all_books.html', {'page_obj': page_obj})


def submit_feedback(request):
    if request.method == 'POST':
        book_id = request.POST.get('book_id')
        feedback_text = request.POST.get('review')
        rating = request.POST.get('rating')

        book = Book.objects.get(id=book_id)
        user = User.objects.get(LOGIN_id=request.session['lid']) 

        existing_feedback = Feedbacks.objects.filter(BOOK=book, USER=user).first()

        if existing_feedback:
            # Feedback already exists; prevent re-submission
            return redirect('/view_published_books')

        # If no existing feedback, create new feedback
        Feedbacks.objects.create(
            BOOK=book,
            USER=user,
            feedback=feedback_text,
            rating=rating,
            date=timezone.now()
        )

        return redirect('/view_published_books')
    else:
        return redirect('/view_published_books')


def book_edit_request(request,id):
    BOOK = Book.objects.get(id=id)
    user = User.objects.get(LOGIN_id=request.session['lid'])

    edit_request = BookEditRequest(BOOK=BOOK,USER=user)
    edit_request.save()
    return HttpResponse('''<script>alert("Request Send Successfully"); window.location='/view_published_books';</script>''')


def view_edit_request(request):
    requests = BookEditRequest.objects.filter(BOOK__USER__LOGIN=request.session['lid'],status='pending')
    return render(request, 'User/view_request.html',{'requests':requests})

def accept_request(request, request_id):
    edit_request = BookEditRequest.objects.get(id=request_id)
    edit_request.status = 'accepted'
    edit_request.save()
    return redirect('/view_edit_request')

def reject_request(request, request_id):
    edit_request = BookEditRequest.objects.get(id=request_id)
    edit_request.status = 'rejected'
    edit_request.save()
    return redirect('/view_edit_request')

def view_accepted_requests(request):
    requests = BookEditRequest.objects.filter(BOOK__USER__LOGIN=request.session['lid'], status='accepted')
    return render(request, 'User/view_accepted_requests.html', {'requests': requests})

def edit_requested_book(request, book_id):
    book = Book.objects.get(id=book_id)
    if request.method == 'POST':
        if 'file' in request.FILES:
            book.file = request.FILES.get('file')
            book.save()
            edit_request = BookEditRequest.objects.get(BOOK=book)
            edit_request.status = 'completed'
            edit_request.save()
        return HttpResponse('''<script>alert("Book Updated Successfully"); window.location='/view_accepted_requests';</script>''')
    return render(request, 'User/edit_requested_book.html', {'book': book})

def manage_profile(request):
    profile = User.objects.get(LOGIN_id=request.session['lid'])
    return render(request, 'User/my_profile.html',{'profile':profile})


def edit_profile(request):
    profile = User.objects.get(LOGIN_id=request.session['lid'])
    if request.method == 'POST':
        profile.name = request.POST['name']
        profile.dob = request.POST['dob']
        profile.phone = request.POST['phone']
        profile.email = request.POST['email']
        profile.place = request.POST['place']
        profile.pin = request.POST['pin']
        profile.post = request.POST['post']
        profile.gender = request.POST['gender']

        if 'photo' in request.FILES:
            profile.photo = request.FILES['photo']

        profile.save()
        return redirect('/manage_profile')
    return render(request, 'User/edit_profile.html', {'profile': profile})

def manage_complaint(request):
    complaint = Complaint.objects.filter(USER__LOGIN=request.session['lid']).order_by('-id')
    return render(request, 'User/manage_complaints.html',{'complaint':complaint})

def add_new_complaint(request):
    if request.method == 'POST':
        complaint = request.POST['complaint']
        com = Complaint(USER=User.objects.get(LOGIN_id=request.session['lid']),complaint=complaint)
        com.save()
        return HttpResponse('''<script>alert("Complaint Added"); window.location='/manage_complaint';</script>''')
    return render(request, 'User/send_complaint.html')


def admin_view_users(request):
    query = request.GET.get('search', '')
    users = User.objects.filter(name__icontains=query).order_by('name')
    paginator = Paginator(users, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'Admin/view_users.html', {'page_obj': page_obj, 'query': query})

def block_user(request,id):
    user = Login.objects.get(id=id)
    user.type = 'blocked'
    user.save()
    return HttpResponse('''<script>alert("Blocked"); window.location='/admin_view_users';</script>''')

def unblock_user(request,id):
    user = Login.objects.get(id=id)
    user.type = 'user'
    user.save()
    return HttpResponse('''<script>alert("Unblocked"); window.location='/admin_view_users';</script>''')

def admin_view_published_books(request):
    books = Book.objects.all().order_by('book_name')
    paginator = Paginator(books, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'Admin/view_books.html', {'page_obj': page_obj})


def admin_view_feedback(request):
    search_query = request.GET.get('search', '')
    if search_query:
        feedbacks = Feedbacks.objects.filter(BOOK__book_name__icontains=search_query).order_by('BOOK__book_name')
    else:
        feedbacks = Feedbacks.objects.all().order_by('BOOK__book_name')

    paginator = Paginator(feedbacks, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'Admin/view_feedbacks.html', {
        'page_obj': page_obj,
        'query': search_query
    })

def admin_manage_complaints(request):
    complaints = Complaint.objects.all()
    return render(request, 'Admin/manage_complaints.html',{'complaints':complaints})

@require_POST
def add_reply(request):
    complaint_id = request.POST.get('complaint_id')
    reply = request.POST.get('reply')

    complaint = Complaint.objects.get(id=complaint_id)
    complaint.reply = reply
    complaint.save()

    return redirect('/admin_manage_complaints')