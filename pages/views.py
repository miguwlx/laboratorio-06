
from django.shortcuts import render
from .models import Resource


def home(request):
    context = {
        "welcome_message": "Explore learning resources and project ideas."
    }
    return render(request, "pages/home.html", context)


def resources(request):
    resources_list = Resource.objects.select_related(
        "category"
    ).all()

    context = {
        "resources": resources_list,
    }
    return render(request, "pages/resources.html", context)


def about(request):
    context = {
        "description": "ClassroomHub is a collaborative learning portal."
    }
    return render(request, "pages/about.html", context)
