from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.db import connection
from django.core.mail import send_mail
from django.conf import settings
from django.utils.html import escape

@csrf_exempt  # A1: Broken Access Control (CSRF not enforced)
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        user = User.objects.create_user(username=username, password=password, email=email)
        return HttpResponse(f"User {escape(user.username)} registered")
    return render(request, 'register.html')

@csrf_exempt  # A2: Cryptographic Failures (password stored, but app allows plaintext transmission)
def login_view(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user:
            login(request, user)
            return HttpResponse("Logged in")
        return HttpResponse("Invalid credentials")
    return render(request, 'login.html')

@csrf_exempt  # A3: Injection (SQL Injection)
def get_user_data(request):
    username = request.GET.get('username')
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT * FROM auth_user WHERE username = '{username}'")
        row = cursor.fetchone()
    return HttpResponse(f"User Data: {row}")

@csrf_exempt  # A4: Insecure Design (No rate limiting, CSRF, or validation)
def contact_admin(request):
    if request.method == 'POST':
        subject = request.POST['subject']
        message = request.POST['message']
        send_mail(subject, message, 'admin@example.com', ['admin@example.com'])
        return HttpResponse("Message sent")
    return render(request, 'contact.html')

@csrf_exempt  # A5: Security Misconfiguration (No HTTPS enforcement, debug enabled)
def show_debug_info(request):
    return HttpResponse(str(settings))

@csrf_exempt  # A6: Vulnerable and Outdated Components (assume older Django used)
def vulnerable_component(request):
    return HttpResponse("This is a known vulnerable endpoint")

@csrf_exempt  # A7: Identification and Authentication Failures (No lockout, weak login)
def brute_force_demo(request):
    return login_view(request)

@csrf_exempt  # A8: Software and Data Integrity Failures (Unvalidated file uploads)
def upload_file(request):
    if request.method == 'POST':
        f = request.FILES['file']
        with open(f.name, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
        return HttpResponse("File uploaded")
    return render(request, 'upload.html')

@csrf_exempt  # A9: Security Logging and Monitoring Failures (no logging at all)
def silent_failure(request):
    return HttpResponse("Something failed silently")

@csrf_exempt  # A10: Server-Side Request Forgery (SSRF)
def ssrf_vuln(request):
    import requests
    url = request.GET.get('url')
    res = requests.get(url)
    return HttpResponse(res.text)
