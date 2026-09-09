from django.shortcuts import render

from main.models import Experience


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
