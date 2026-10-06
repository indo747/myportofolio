from django.core.exceptions import ValidationError
from django.forms import DateInput, DateTimeInput, ModelForm, Select, Textarea, TextInput, URLInput

from django.utils.html import strip_tags

from main.models import Education, Experience


class EducationForm(ModelForm):
    class Meta:
        model = Education
        fields = ["degree", "institution", "level", "description", "started_at", "ended_at"]

        labels = {
            "degree": "Degree",
            "institution": "Institution",
            "level": "Level",
            "description": "Description",
            "started_at": "Start date",
            "ended_at": "End date (leave empty if still ongoing)",
        }

        widgets = {
            "degree": TextInput(attrs={"placeholder": "MSc Computer Science", "maxlength": 255}),
            "institution": TextInput(attrs={"placeholder": "TU Darmstadt", "maxlength": 255}),
            "level": Select(),
            "description": Textarea(attrs={"placeholder": "Focus, thesis or anything else worth mentioning", "rows": 3}),
            # type=date gives a date picker in the browser, the format has to be ISO for that to work
            "started_at": DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
            "ended_at": DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
        }


class ExperienceForm(ModelForm):
    class Meta:
        model = Experience
        # started_at is filled in by the model itself, so it must not be offered here
        fields = ["title", "description", "category", "thumbnail", "ended_at"]

        labels = {
            "title": "Role",
            "description": "Description",
            "category": "Type of work",
            "thumbnail": "Image URL (optional)",
            "ended_at": "End date (leave empty if still ongoing)",
        }

        widgets = {
            "title": TextInput(attrs={"placeholder": "IT Consultant", "maxlength": 255}),
            "description": Textarea(attrs={"placeholder": "What you did and what you took from it", "rows": 3}),
            "category": Select(),
            "thumbnail": URLInput(attrs={"placeholder": "https://example.com/logo.png"}),
            # datetime-local only prefills when the value is rendered in exactly this format
            "ended_at": DateTimeInput(attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"),
        }

    def clean_title(self):
        title = strip_tags(self.cleaned_data["title"]).strip()
        if not title:
            raise ValidationError("Role can't consist of HTML tags only.")
        return title

    def clean_description(self):
        description = strip_tags(self.cleaned_data["description"]).strip()
        if not description:
            raise ValidationError("Description can't consist of HTML tags only.")
        return description
