import datetime

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import PermissionDenied
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from main.forms import EducationForm, ExperienceForm
from main.models import Education, Experience

EDITOR_GROUP = "Editor"


def is_editor(user):
    return user.is_authenticated and user.groups.filter(name=EDITOR_GROUP).exists()


def may_edit(user):
    # the owner may do everything, an editor may only change what already exists
    return user.is_superuser or is_editor(user)


def show_main(request):
    last_login = request.COOKIES.get("last_login", "No active login session / Cookie not found")
    context = {
        "name": "Tahir Ahmad",
        "last_login": last_login,
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
    # the page only ships the skeleton now, the entries arrive through the JSON endpoint
    title_query = request.GET.get("title", "").strip()

    context = {
        "name": "Tahir Ahmad",
        "title_query": title_query,
        "can_edit": may_edit(request.user),
        "form": ExperienceForm(),
    }
    return render(request, "experience.html", context)


def get_experience_json(request):
    title_query = request.GET.get("title", "").strip()
    experience = Experience.objects.prefetch_related("starred_by").all()

    if title_query:
        experience = experience.filter(title__icontains=title_query)

    # built by hand because the built in serializer cannot tell who is signed in
    data = []
    for entry in experience:
        starred_users = entry.starred_by.all()
        data.append({
            "pk": str(entry.id),
            "fields": {
                "title": entry.title,
                "description": entry.description,
                "category": entry.get_category_display(),
                "is_ongoing": entry.is_ongoing,
                "star_count": starred_users.count(),
                "is_starred": request.user in starred_users if request.user.is_authenticated else False,
                "starred_by_names": ", ".join(user.username for user in starred_users),
            },
        })

    return JsonResponse(data, safe=False)


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
        "can_edit": may_edit(request.user),
    }
    return render(request, "education.html", context)


def get_education_json(request):
    degree_query = request.GET.get("degree", "").strip()
    education = Education.objects.all()

    if degree_query:
        education = education.filter(degree__icontains=degree_query)

    education_json = serializers.serialize("json", education)
    return HttpResponse(education_json, content_type="application/json")


@login_required(login_url="/login/")
def create_education(request):
    if not request.user.is_superuser:
        raise PermissionDenied

    form = EducationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "New education entry added.")
        return redirect("main:show_education")

    context = {
        "name": "Tahir Ahmad",
        "form": form,
        "heading": "Add Education",
        "submit_label": "Add Education",
    }
    return render(request, "education_form.html", context)


@login_required(login_url="/login/")
def update_education(request, education_id):
    if not may_edit(request.user):
        raise PermissionDenied

    education = get_object_or_404(Education, pk=education_id)
    form = EducationForm(request.POST or None, instance=education)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Education entry updated.")
        return redirect("main:show_education")

    context = {
        "name": "Tahir Ahmad",
        "form": form,
        "heading": "Edit Education",
        "submit_label": "Save changes",
    }
    return render(request, "education_form.html", context)


@login_required(login_url="/login/")
def delete_education(request, education_id):
    if not request.user.is_superuser:
        raise PermissionDenied

    education = get_object_or_404(Education, pk=education_id)

    # only POST deletes, so following a plain link can never remove anything
    if request.method == "POST":
        education.delete()
        messages.success(request, "Education entry deleted.")

    return redirect("main:show_education")


@login_required(login_url="/login/")
def create_experience(request):
    if not request.user.is_superuser:
        raise PermissionDenied

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


@login_required(login_url="/login/")
def update_experience(request, experience_id):
    if not may_edit(request.user):
        raise PermissionDenied

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


@login_required(login_url="/login/")
def delete_experience(request, experience_id):
    if not request.user.is_superuser:
        raise PermissionDenied

    experience = get_object_or_404(Experience, pk=experience_id)

    if request.method == "POST":
        experience.delete()
        messages.success(request, "Experience entry deleted.")

    return redirect("main:show_experience")


def register(request):
    form = UserCreationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Account created successfully. Please log in.")
        return redirect("main:login")

    context = {
        "name": "Tahir Ahmad",
        "form": form,
    }
    return render(request, "register.html", context)


def login_user(request):
    # named login_user so it does not shadow the imported login function
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        login(request, form.get_user())
        response = redirect("main:show_main")
        # the session already identifies the user, this cookie only shows them when they last signed in
        response.set_cookie("last_login", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        return response

    context = {
        "name": "Tahir Ahmad",
        "form": form,
    }
    return render(request, "login.html", context)


def logout_user(request):
    logout(request)
    response = redirect("main:show_main")
    response.delete_cookie("last_login")
    return response


# no is_superuser check here, every signed in account may star an entry
@login_required(login_url="/login/")
def toggle_star(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)

    if request.method == "POST":
        if request.user in experience.starred_by.all():
            experience.starred_by.remove(request.user)
        else:
            experience.starred_by.add(request.user)

    return redirect("main:show_experience")


@require_POST
def create_experience_ajax(request):
    # no @login_required here on purpose: it answers with a redirect to the login page,
    # and fetch would follow that and read the login HTML as a success
    if not request.user.is_superuser:
        return JsonResponse(
            {"message": "Only the portfolio owner can add entries."},
            status=403,
        )

    form = ExperienceForm(request.POST)
    if form.is_valid():
        experience = form.save()
        return JsonResponse(
            {"message": "Experience added successfully.", "pk": str(experience.id)},
            status=201,
        )

    return JsonResponse({"errors": form.errors.get_json_data()}, status=400)
