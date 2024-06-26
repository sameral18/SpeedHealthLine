# Generated by Django 5.0.3 on 2024-03-28 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_alter_calendar_options_calendar_description_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='calendar',
            name='description',
        ),
        migrations.RemoveField(
            model_name='calendar',
            name='patient',
        ),
        migrations.RemoveField(
            model_name='calendar',
            name='status',
        ),
        migrations.AddField(
            model_name='calendar',
            name='is_available',
            field=models.BooleanField(default=True),
        ),
    ]
