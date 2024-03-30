# Generated by Django 5.0.3 on 2024-03-30 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_remove_appointment_doctorid_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='doctorId',
            field=models.PositiveIntegerField(default=0, null=True),
        ),
        migrations.AddField(
            model_name='appointment',
            name='patientId',
            field=models.PositiveIntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='timeslots',
            field=models.ManyToManyField(null=True, to='core.doctorschedule'),
        ),
    ]