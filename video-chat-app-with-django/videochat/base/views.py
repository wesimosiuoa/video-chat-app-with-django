from django.shortcuts import render, redirect
from django.utils.translation import gettext as _
from django.http import JsonResponse
from agora_token_builder import RtcTokenBuilder
import random
import time
from django.http import HttpResponseRedirect
import json
from django.utils import translation
from django.conf import settings 
from .models import RoomMember
from .models import Post
from .models import Notifications
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
# from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login as auth_login
from .serializers import PostSerializer



@transaction.atomic
#Build token with uid
def getToken (request):
    appId =  '4fcd24e9e7c741c9902a5ac0a9313947'
    appCertificate = 'd5e2e24da6d84d07b7dc98b081cfe067'
    channelName = request.GET.get('channel')
    uid = random.randint (1, 230)
    expirationTimeInSeconds = 3600 * 24
    currentTimeStamp = time.time()
    privilegeExpiredTs = currentTimeStamp + expirationTimeInSeconds
    role = 1
    token = RtcTokenBuilder.buildTokenWithUid(appId, appCertificate, channelName, uid, role, privilegeExpiredTs)
    return JsonResponse({'token': token, 'uid' : uid}, safe=False)
# Create your views here.

from django.contrib import messages
from django.shortcuts import render, redirect


@csrf_exempt  # Allows the view to receive a POST request without CSRF token (or you can use CSRF token if passed)
def create_notification(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        sender = data.get('sender')
        body = data.get('body')

        # Create the notification in the database
        Notifications.objects.create(sender=sender, body=body)
        
        return JsonResponse({'status': 'Notification created successfully'}, status=201)
    return JsonResponse({'error': 'Invalid request'}, status=400)


#translation 

def my_view (request): 
    greeting = _(" Hello, world ")
#translation end here 
from django.utils import translation
from django.shortcuts import redirect

@csrf_exempt
def set_language(request):
    user_language = request.POST.get('language')
    translation.activate(user_language)
    # Use the string 'django_language' directly
    request.session['django_language'] = user_language
    return redirect(request.META.get('HTTP_REFERER', '/'))

def notifications (request): 
    notifications = Notifications.objects.all().order_by ('-created')
    notification_count = notifications.count()
    
    print ('Number of notifications \n ', notification_count)
    return render (request, 'base/notification.html',  {'notifications':notifications, 'notification_count':notification_count})
@csrf_exempt
def login(request):
    if request.method == 'POST': 
        username = request.POST.get('email')
        password = request.POST.get('password')

        if not username or not password:
            messages.error(request, 'Username and password are required.')
            return redirect('welcome')  # Redirect back to the welcome page
        
        user = authenticate (request, username = username, password = password)

        if user is not None: 
            auth_login (request, user)
            request.session['username'] = username
            messages.success( request, 'Login successful ')
            return redirect ('home')
        else:
            messages.error(request, f'Invalid login details  - Username : {username} and Password : {password}  ')
            return redirect('welcome')  # Redirect to another page after success

    return render(request, 'base/welcome.html')
    
def register(request): 
    if request.method == 'POST': 
        username = request.POST.get('registerName')
        email = request.POST.get('registerEmail')
        passwordString = request.POST.get('registerPassword')
        confirm_password = request.POST.get('registerConfirmPassword')

        # Check if passwords match
        if passwordString != confirm_password: 
            messages.error(request, 'Passwords do not match.')
            return redirect('welcome')
        
        # Check for existing username or email
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('welcome')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email is already registered.')
            return redirect('welcome')

        try:
            # Create the user using the create_user method
            user = User.objects.create_user(
                username=username, 
                email=email, 
                password = make_password(passwordString)
            )
            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('welcome')  # Redirect to the login page after successful registration

        except Exception as e: 
            messages.error(request, f'Error during registration: {e}')
            print(f' Error : {e}')
            return redirect('welcome')  # Redirect back to the welcome page in case of an error

    return render(request, 'base/welcome.html')

def welcome (request):
    return render (request, 'base/welcome.html')
def index(request): 
    return render (request, 'base/index.html')
def home (request): 
    return render (request, 'base/home.html')
def room(request): 
    return render (request, 'base/room.html')
def discussion (request): 
    
    posts = Post.objects.all().order_by('-created')
    context = {'posts':posts}
    return render (request, 'base/discussion.html', context)

@api_view(['POST'])
def add_post(request): 
    data = request.data
    print (' Data : ', data)
    
    post = Post.objects.create(
        sender = request.session['username'],
        body = data['body']
    )
    sender = request.session['username']
    notification = Notifications.objects.create (
        sender = request.session['username'], 
        body = f' You have new message from {sender} in group chat main'
    )
    serializer = PostSerializer(post, many = False)
    
    return Response(serializer.data)


@csrf_exempt
def createUser(request):
    try:
        data = json.loads(request.body)
        member, created = RoomMember.objects.get_or_create(
            name = data['name'], 
            uid = data['UID'], 
            room_name = data['room_name']
        )
        return JsonResponse({'name': data['name']}, safe=False)
    
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def get_member (request): 
    uid = request.GET.get('UID')
    room_name = request.GET.get('room_name')

    member = RoomMember.objects.get(
        uid = uid , 
        room_name = room_name, 
    )
    name = member.name
    return JsonResponse({'name': member.name}, safe=False)


@csrf_exempt
def deleteMember (request): 
    data = json.loads(request.body)
    member = RoomMember.objects.get(
        name = data['name'],
        uid = data['uid'],
        room_name = data['room_name'], 
    )
    member.delete()
    return JsonResponse(' Member was deleted ', safe=False)

from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to the login page
