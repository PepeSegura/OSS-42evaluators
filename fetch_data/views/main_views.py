import logging

from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.urls import reverse

from datetime import datetime
import pytz

from django.db.models import Subquery, OuterRef, FloatField, Value
from django.db.models.functions import Coalesce
from django.db.models import Case, When, FloatField, Value, IntegerField
from fetch_data.models import Piscine, Cursus, Project, ClusterLocation
from fetch_data.models import User as OurUser

from fetch_data.forms import FavoriteUsersForm

logger = logging.getLogger(__name__)

#USED /cursus -> My Cursus
@login_required(login_url='/login/42')  # Redirect to login_42 if not logged in
def cursus(request):
    context = {}
    login = request.GET.get('user', request.user.username)
    page = request.GET.get('page', '1')
    items_per_page = 50
    if int(page) < 1:
        page = '1'

    paginator = Paginator(Cursus.objects.filter(user__login=login), items_per_page)
    paginated_cursus = paginator.get_page(page)

    # Convert marked_at to datetime object
    for cursus in paginated_cursus:
        if isinstance(cursus.begin_at, str):
            cursus.begin_at = datetime.strptime(cursus.begin_at, "%Y-%m-%dT%H:%M:%S.%fZ")
        if isinstance(cursus.blackholed_at, str):
            cursus.blackholed_at = datetime.strptime(cursus.blackholed_at, "%Y-%m-%dT%H:%M:%S.%fZ")

    context['login'] = login
    context['title'] = login + '\'s Cursus'
    context['cursus'] = paginated_cursus
    context['page'] = page
    if 'HX-Request' in request.headers:
        return render(request, 'cursus/cursus.html', context)
    else:
        return render(request, 'cursus/cursus_full.html', context)

#USED /projects -> My Projects
@login_required(login_url='/login/42')  # Redirect to login_42 if not logged in
def projects(request):
    items_per_page = 50
    context = {}
    login = request.GET.get('user', request.user.username)
    page = request.GET.get('page', '1')
    if int(page) < 1:
        page = '1'

    paginator = Paginator(Project.objects.filter(user__login=login), items_per_page)
    paginated_projects = paginator.get_page(page)

    # Convert marked_at to datetime object
    for project in paginated_projects:
        if isinstance(project.marked_at, str):
            project.marked_at = datetime.strptime(project.marked_at, "%Y-%m-%dT%H:%M:%S.%fZ")

    offset = (int(page) - 1) * items_per_page
    context['login'] = login
    context['title'] = login + '\'s Projects'
    context['projects'] = paginated_projects
    context['page'] = page
    context['offset'] = offset
    if 'HX-Request' in request.headers:
        return render(request, 'projects/projects.html', context)
    else:
        return render(request, 'projects/projects_full.html', context)

#USED /all-project -> Latest project
@login_required(login_url='/login/42')  # Redirect to login_42 if not logged in
def allprojects(request):
    items_per_page = 50
    context = {}
    page = request.GET.get('page', '1')
    if int(page) < 1:
        page = '1'

    paginator = Paginator(Project.objects.all(), items_per_page)
    paginated_projects = paginator.get_page(page)

    # Convert marked_at to datetime object
    for project in paginated_projects:
        if isinstance(project.marked_at, str):
            project.marked_at = datetime.strptime(project.marked_at, "%Y-%m-%dT%H:%M:%S.%fZ")

    offset = (int(page) - 1) * items_per_page
    context['login'] = '42Madrid'
    context['title'] = '42 Madrid\'s Projects'
    context['projects'] = paginated_projects
    context['page'] = page
    context['offset'] = offset
    if 'HX-Request' in request.headers:
        return render(request, 'projects/projects.html', context)
    else:
        return render(request, 'projects/projects_full.html', context)


#USED /peers -> Peers+
@login_required(login_url='/login/42')  # Redirect to login_42 if not logged in
def peers(request):
    context = {}
    context['title'] = 'peers+ config'
    context['owner'] = ''
    context['login'] = ''
    context['favorites'] = []  # Users marked as favorites by `owner`
    context['favorited_by'] = []  # Users who have marked `owner` as favorite
    form = FavoriteUsersForm()
    try:
        login = request.GET.get('user', request.user.username)
        owner = OurUser.objects.filter(login=login).first()
        if owner is None:
            raise ValueError(f"User not found: {login}")

        context['title'] = 'peers+ config'
        context['owner'] = owner
        context['login'] = owner.login
        context['favorites'] = owner.favorite_users.all()  # Users marked as favorites by `owner`
        context['favorited_by'] = owner.favorited_by.all()  # Users who have marked `owner` as favorite
        context['error_message'] = None

        if request.method == 'POST':
            if 'action' in request.POST:
                action = request.POST.get('action')
                if action == 'add':
                    new_friend_login = request.POST.get('new_friend_name')
                    if not new_friend_login or new_friend_login is None:
                        raise ValueError(f"Empty user")
                    new_friend_login = str(new_friend_login).lower()
                    new_friend = OurUser.objects.filter(login=new_friend_login).first()
                    if not new_friend or new_friend is None:
                        raise ValueError(f"User [{new_friend_login}] not found.")
                    if new_friend:
                        owner.favorite_users.add(new_friend)
                elif action == 'delete':
                    friend_id = request.POST.get('user_id')
                    friend = OurUser.objects.filter(id=friend_id).first()
                    if not friend or friend is None:
                        raise ValueError("Friend not found.")
                    else:
                        owner.favorite_users.remove(friend)
                return redirect('peers')
        context['form'] = form
    except Exception as e:
        context['error_message'] = str(e)

    if 'HX-Request' in request.headers:
        return render(request, 'peers/peers.html', context)
    else:
        return render(request, 'peers/peers_full.html', context)

#IN PROGRESS /add
@login_required(login_url='/login/42')  # Redirect to login_42 if not logged in
def add_friend(request):
    username_query = request.GET.get('username', '')

    if not username_query:
        return HttpResponseBadRequest("No username provided.")

    new_friend = OurUser.objects.filter(login=username_query).first()

    if not new_friend:
        return HttpResponseBadRequest("User not found.")

    owner = request.user

    if owner == new_friend:
        return HttpResponseBadRequest("Cannot add yourself as a friend.")

    owner = OurUser.objects.filter(login=owner).first()
    owner.favorite_users.add(new_friend)

    # Redirect to a success page or back to the previous page
    return HttpResponseRedirect(reverse('clusters'))


#USED /clusters -> Clusters
@login_required(login_url='/login/42')  # Redirect to login_42 if not logged in
def cluster_view(request):
    developers = {"psegura-", "sacorder"}
    context = {}
    context['title'] = "42 Madrid's Clusters"

    login = request.GET.get('user', request.user.username)
    owner = OurUser.objects.filter(login=login).first()

    context['owner'] = owner
    context['login'] = str(login)

    favorites    = []
    favorited_by = []

    if owner:
        favorites = owner.favorite_users.all()
        favorited_by = owner.favorited_by.all()

    context['favorites'] = favorites
    context['favorited_by'] = favorited_by

    rowsc1, rowsc2, rowsc3 = [], [], []
    occupancy_c1, occupancy_c2, occupancy_c3 = 0, 0, 0

    def get_row_data(cluster_number, rows):
        occupancy_counter = 0
        for i in range(17, 0, -1) if cluster_number == 1 else range(19, 0, -1) if cluster_number == 2 else range(14, 0, -1):
            row_data = {
                'row_label': f'r{i}',
            }
            for j in range(1, 7):  # For s1 to s6
                host = f'c{cluster_number}r{i}s{j}'  # Construct the host value
                # Query ClusterLocation to get the object with the constructed host value
                location = ClusterLocation.objects.filter(host=host).first()
                if location:
                    occupancy_counter += 1
                    # Check if the location's user is a favorite or favorited_by
                    location.is_favorite = location.user in favorites
                    location.is_favorited_by = location.user in favorited_by
                    location.is_dev = str(location.user) in developers
                    location.is_owner = False
                    if owner:
                        location.is_owner = str(location.user) == str(owner.login)
                row_data[f's{j}'] = location
            rows.append(row_data)
        return occupancy_counter

    # Populate row data for each cluster
    occupancy_c1 = get_row_data(1, rowsc1)
    occupancy_c2 = get_row_data(2, rowsc2)
    occupancy_c3 = get_row_data(3, rowsc3)

    context['rowsc1'] = rowsc1
    context['rowsc2'] = rowsc2
    context['rowsc3'] = rowsc3

    # Add occupancy to context
    context['occupancy'] = [occupancy_c1, occupancy_c2, occupancy_c3]
    if 'HX-Request' in request.headers:
        return render(request, 'clusters/clusters.html', context)
    else:
        return render(request, 'clusters/clusters_full.html', context)


#USED /index -> Students / 42 Madrid's Evaluators
@login_required(login_url='/login/42')  # Redirect to login_42 if not logged in
def index(request):
    context = {}
    items_per_page = 50
    sort_by = request.GET.get('sort_by', '-cursus_21_level')
    search_query = request.GET.get('search', '')
    page = request.GET.get('page', '1')
    piscine_id = request.GET.get('piscine', None)

    # Ensure page number is valid
    try:
        page = int(page)
        if page < 1:
            page = 1
    except ValueError:
        page = 1

    # Fetch users and filter by search query
    users = OurUser.objects.filter(login__icontains=search_query) if search_query else OurUser.objects.all()

    # Filter by piscine if provided
    if piscine_id and piscine_id.isdigit():
        users = users.filter(piscine_id=int(piscine_id))

    # Determine selected piscine
    selected_piscine = Piscine.objects.filter(id=piscine_id).first() if piscine_id and piscine_id.isdigit() else None

    # Subqueries for cursus levels
    cursus_21_level = Cursus.objects.filter(user=OuterRef('pk'), cursus_id=21).values('level')[:1]
    cursus_9_level = Cursus.objects.filter(user=OuterRef('pk'), cursus_id=9).values('level')[:1]

    # Annotate users with cursus levels
    users = users.annotate(
        cursus_21_level=Coalesce(Subquery(cursus_21_level, output_field=FloatField()), Value(0.0)),
        cursus_9_level=Coalesce(Subquery(cursus_9_level, output_field=FloatField()), Value(0.0)),
    ).order_by(sort_by).distinct()

    # Pagination
    paginator = Paginator(users, items_per_page)
    paginated_users = paginator.get_page(page)

    # Offset calculation
    offset = (paginated_users.number - 1) * items_per_page

    # Context data
    context['users'] = paginated_users
    context['title'] = 'Leaderboard'
    context['page'] = page
    context['search_query'] = search_query
    context['sort_by'] = sort_by
    context['sort_dir'] = '' if sort_by.startswith('-') else '-'
    context['offset'] = offset
    context['piscines'] = Piscine.objects.all()
    context['selected_piscine'] = selected_piscine
    if 'HX-Request' in request.headers:
        return render(request, 'leaderboard/leaderboard.html', context)
    else:
        return render(request, 'leaderboard/leaderboard_full.html', context)

