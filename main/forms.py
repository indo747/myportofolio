from django.forms import DateInput, ModelForm, Select, Textarea, TextInput

from main.models import Education


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
