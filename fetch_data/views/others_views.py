import logging

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse

from fetch_data.models import UsefulLink
from fetch_data.models import Cursus, Project
from fetch_data.models import User as OurUser

logger = logging.getLogger(__name__)

def about(request):
    context = {}
    context['title'] = 'About'
    useful_links = UsefulLink.objects.all()
    context['useful_links'] = useful_links
    return render(request, 'about.html', context)

@login_required(login_url='/login/42')  # Redirect to login_42 if not logged in
def calculator(request):
    print(f"request: {request}")
    context = {}
    context['title'] = 'Calculator'
    login = request.GET.get('user', request.user.username)
    owner = OurUser.objects.filter(login=login).first()
    owner_cursus = Cursus.objects.filter(user=owner, cursus_id=21).first()
    owner_projects = Project.objects.filter(user=owner, cursus_id=21)

    context['owner_projects'] = owner_projects
    context['owner_cursus'] = owner_cursus
    return render(request, 'calculator.html', context)
