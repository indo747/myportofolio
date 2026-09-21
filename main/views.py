from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from main.forms import EducationForm, ExperienceForm
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
    # the page reads from the same JSON endpoint as external clients, so the search filter lives in one place
    json_response = get_education_json(request)

    entries = serializers.deserialize("json", json_response.content.decode("utf-8"))
    entries = [entry.object for entry in entries]
    degree_query = request.GET.get("degree", "").strip()

    context = {
        "name": "Tahir Ahmad",
        "education_list": entries,
        "degree_query": degree_query,
    }
    return render(request, "education.html", context)


def get_education_json(request):
    degree_query = request.GET.get("degree", "").strip()
    education = Education.objects.all()

    if degree_query:
        education = education.filter(degree__icontains=degree_query)

    education_json = serializers.serialize("json", education)
    return HttpResponse(education_json, content_type="application/json")


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


def delete_education(request, education_id):
    education = get_object_or_404(Education, pk=education_id)

    # only POST deletes, so following a plain link can never remove anything
    if request.method == "POST":
        education.delete()
        messages.success(request, "Education entry deleted.")

    return redirect("main:show_education")


def create_experience(request):
    form = ExperienceForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "New experience entry added.")
        return redirect("main:show_experience")

    context = {
        "name": "Tahir Ahmad",
        "form": form,
        "heading": "Add Experience",
        "submit_label": "Add Experience",
    }
    return render(request, "experience_form.html", context)


def update_experience(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)
    # instance= turns the same form class into an edit form, prefilled and saving back onto that row
    form = ExperienceForm(request.POST or None, instance=experience)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Experience entry updated.")
        return redirect("main:show_experience")

    context = {
        "name": "Tahir Ahmad",
        "form": form,
        "heading": "Edit Experience",
        "submit_label": "Save changes",
    }
    return render(request, "experience_form.html", context)
