from django.contrib import messages
from django.shortcuts import redirect, render

from main.forms import EducationForm
from main.models import Education, Experience


def show_main(request):
    context = {
        "name": "Tahir Ahmad",
        "npm": "2606816466",
        "study_program": "Master Computer Science",
        "bio": (
            "I'm a Computer Science Master's student from Germany, spending this semester "
            "at Universitas Indonesia as an exchange student. Back home I work as an IT "
            "consultant, taught as a tutor at my university and still give private lessons "
            "on the side. In my free time I play squash, train at the gym and here in "
            "Indonesia I've started learning guitar."
        ),
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": "Tahir Ahmad",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)


def show_education(request):
    context = {
        "name": "Tahir Ahmad",
        "education_list": Education.objects.all(),
    }
    return render(request, "education.html", context)


def create_education(request):
    form = EducationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "New education entry added.")
        return redirect("main:show_education")

    context = {
        "name": "Tahir Ahmad",
        "form": form,
    }
    return render(request, "education_form.html", context)
