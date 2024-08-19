from update_database.our_network_manager import updateTokenInfo, needToUpdate

import sys, random, string, requests, time, threading
from queue import Queue

from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse
from django.urls import reverse

from fetch_data.models import Key, Cursus

# Rate limiting parameters
MAX_REQUESTS_PER_SECOND = 2
REQUEST_INTERVAL = 1 / MAX_REQUESTS_PER_SECOND

# A simple queue to manage incoming requests
request_queue = Queue()

# Lock for synchronized access
lock = threading.Lock()

# Store user information based on session keys
pending_requests = {}

# Worker function to process the queue
def process_queue():
    while True:
        # Get the next request from the queue
        user_info_url, headers, session_key = request_queue.get()

        # Process the request
        user_info_response = requests.get(user_info_url, headers=headers)
        user_info = user_info_response.json()

        # Store the user info based on session key
        with lock:
            pending_requests[session_key] = user_info

        # Wait to maintain the rate limit
        time.sleep(REQUEST_INTERVAL)

        # Mark the task as done
        request_queue.task_done()

# Start the queue processing thread
thread = threading.Thread(target=process_queue, daemon=True)
thread.start()

# Function to add requests to the queue
def add_request_to_queue(user_info_url, headers, session_key):
    request_queue.put((user_info_url, headers, session_key))

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)
# Create your views here.

def generate_state():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=40))

def login_42(request):
    if request.user.is_authenticated:
        return redirect('index')

    client_id = Key.objects.filter(name='1_LOGIN').first().uid
    redirect_uri = 'http://127.0.0.1:8000/auth/callback'
    scope = 'public'
    state = generate_state()
    request.session['oauth_state'] = state
    authorize_url = (
        f"https://api.intra.42.fr/oauth/authorize?client_id={client_id}"
        f"&redirect_uri={redirect_uri}&response_type=code&state={state}"
    )
    return redirect(authorize_url)

def landing(request):
    if request.user.is_authenticated:
        return redirect('index')
    return render(request, 'landing.html')


# The callback function to handle the response
def handle_user_info_response(request, user_info):
    username = user_info['login']
    user, created = User.objects.get_or_create(username=username)
    login(request, user)
    return redirect('index')

def auth_callback(request):
    code = request.GET.get('code')
    state = request.GET.get('state')
    if state != request.session.pop('oauth_state', None):
        return HttpResponseBadRequest('Invalid state parameter')

    token_url = 'https://api.intra.42.fr/oauth/token'
    client_id = Key.objects.filter(name='1_LOGIN').first().uid
    client_secret = Key.objects.filter(name='1_LOGIN').first().secret
    # Check and update token info if needed
    leaderboard_token = Key.objects.filter(name='1_LOGIN').first()
    if needToUpdate(leaderboard_token):
        updateTokenInfo(leaderboard_token, client_id, client_secret)
    redirect_uri = 'http://127.0.0.1:8000/auth/callback'

    data = {
        'grant_type': 'authorization_code',
        'client_id': client_id,
        'client_secret': client_secret,
        'code': code,
        'redirect_uri': redirect_uri,
    }

    response = requests.post(token_url, data=data)
    response_data = response.json()

    access_token = response_data.get('access_token')
    eprint(f"Access token received: {access_token}")

    # Use the access token to get user info
    user_info_url = 'https://api.intra.42.fr/v2/me'
    headers = {'Authorization': f'Bearer {access_token}'}
    
    # Add the request to the queue instead of directly making the request
    session_key = request.session.session_key
    add_request_to_queue(user_info_url, headers, session_key)

    return render(request, 'auth_callback.html')

# Endpoint to poll the status of the login request

def check_login_status(request):
    session_key = request.session.session_key

    with lock:
        if session_key in pending_requests:
            user_info = pending_requests.pop(session_key)
            handle_user_info_response(request, user_info)
            return JsonResponse({'status': 'complete', 'redirect_url': reverse('index')})

    return JsonResponse({'status': 'pending'})


def logout_view(request):
    logout(request)
    return redirect('/')  # Redirect to the homepage or any other page after logout