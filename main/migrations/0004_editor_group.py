from django.db import migrations

EDITOR_GROUP = "Editor"


def create_editor_group(apps, schema_editor):
    # the group has to exist on every machine, members are assigned through the admin
    Group = apps.get_model("auth", "Group")
    Group.objects.get_or_create(name=EDITOR_GROUP)


def remove_editor_group(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    Group.objects.filter(name=EDITOR_GROUP).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0003_experience_starred_by"),
        ("auth", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_editor_group, remove_editor_group),
    ]
