from email import message
from django.shortcuts import render, redirect, get_object_or_404  # Added get_object_or_404 # type: ignore
from django.http import HttpResponse # type: ignore
from django.core.mail import send_mail # type: ignore
from django.contrib.auth.models import User  # type: ignore
from django.contrib import messages # type: ignore
from django.contrib.auth import login, authenticate# type: ignore
from django import forms# type: ignore
from django.contrib.auth.decorators import login_required# type: ignore
from .models import NewsPost, Comment
from .forms import CommentForm  # Ensure you created this

# Home page
def index(request):
    return render(request, 'html/index.html')

# Fully functional news page
@login_required
def news(request):
    posts = NewsPost.objects.all().order_by('-created_at')

    # Handle Like
    if request.method == 'POST' and 'like_post_id' in request.POST:
        post_id = request.POST.get('like_post_id')
        post = get_object_or_404(NewsPost, id=post_id)
        if request.user in post.likes.all():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)
        return redirect('news')

    # Handle Comment
    if request.method == 'POST' and 'comment_post_id' in request.POST:
        post_id = request.POST.get('comment_post_id')
        comment_post = get_object_or_404(NewsPost, id=post_id)
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = comment_post
            comment.author = request.user
            comment.save()
        return redirect('news')

    comment_form = CommentForm()
    return render(request, 'html/news.html', {
        'posts': posts,
        'comment_form': comment_form
    })

# Beta reader form
def beta(request):
    if request.method == "POST":
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        reason = request.POST.get('Why')
        gender = request.POST.get('gender')
        birthday = request.POST.get('date')
        region = request.POST.get('region')
        email = request.POST.get('email')
        number = request.POST.get('number')
        genres = request.POST.getlist('genres')

        message = f"""
        New Beta Reader Sign-Up:

        Name: {name} {surname}
        Email: {email}
        Phone: {number}
        Birthday: {birthday}
        Gender: {gender}
        Region: {region}
        Genres: {', '.join(genres)}
        Reason: {reason}
        """

        send_mail(
            subject='New Beta Reader Submission',
            message=message,
            from_email='jad3lbr@gmail.com',
            recipient_list=['jad3lbr@gmail.com'], 
            fail_silently=False,
        )

        return render(request, 'html/thankyou.html', {'name': name})

    return render(request, 'html/Betareader.html')

# Login
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome, {username}!")
            return redirect('index')
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')

    return render(request, 'html/login.html')

# Store
def store(request):
    return render(request, 'html/store.html')

# Contact form
def contact(request):
    if request.method == "POST":
        email = request.POST.get('email')
        message = request.POST.get('message')

        send_mail(
            subject='Contact Form Message',
            message=f"From: {email}\n\nMessage:\n{message}",
            from_email='jad3lbr@gmail.com',
            recipient_list=['jad3lbr@gmail.com'],
            fail_silently=False,
        )

    return render(request, 'html/contact.html')

# Sign-up
def sign_up(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return redirect('signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect('signup')

        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()
        messages.success(request, "Account created successfully.")
        return redirect('login')

    return render(request, 'html/signup.html')
