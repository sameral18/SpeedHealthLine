# Generated by Django 5.0.3 on 2024-04-06 12:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_alter_patientdischargedetails_patientid_message'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Message',
        ),
    ]
