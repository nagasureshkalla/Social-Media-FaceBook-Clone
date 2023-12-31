# Generated by Django 4.0.4 on 2022-06-12 16:19

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_alter_clinic_createddate_alter_clinic_updateddate_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clinic',
            name='createdDate',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 12, 16, 19, 19, 33332), verbose_name='Clinic created At'),
        ),
        migrations.AlterField(
            model_name='clinic',
            name='updatedDate',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 12, 16, 19, 19, 33340), verbose_name='Clinic Last Updated At'),
        ),
        migrations.AlterField(
            model_name='doctor',
            name='createdDate',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 12, 16, 19, 19, 33707), verbose_name='Clinic created At'),
        ),
        migrations.AlterField(
            model_name='doctor',
            name='updatedDate',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 12, 16, 19, 19, 33714), verbose_name='Clinic Last Updated At'),
        ),
        migrations.AlterField(
            model_name='doctorbooking',
            name='createdDate',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 12, 16, 19, 19, 34062), verbose_name='Slot created At'),
        ),
        migrations.AlterField(
            model_name='doctorbooking',
            name='paymentStatus',
            field=models.IntegerField(default=0, max_length=1),
        ),
        migrations.AlterField(
            model_name='doctorbooking',
            name='updatedDate',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 12, 16, 19, 19, 34070), verbose_name='Slot Last Updated At'),
        ),
        migrations.AlterField(
            model_name='messages',
            name='createdDate',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 12, 16, 19, 19, 30934), verbose_name='Chat Last created At'),
        ),
        migrations.AlterField(
            model_name='messages',
            name='updatedDate',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 12, 16, 19, 19, 30942), verbose_name='Chat Last updated At'),
        ),
        migrations.AlterField(
            model_name='post',
            name='createdDate',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 12, 16, 19, 19, 30002), verbose_name='Post Last created At'),
        ),
        migrations.AlterField(
            model_name='post',
            name='updatedDate',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 12, 16, 19, 19, 30013), verbose_name='Post Last Updated At'),
        ),
        migrations.AlterField(
            model_name='postuploaddetails',
            name='createdDate',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 12, 16, 19, 19, 30305), verbose_name='Post Last created At'),
        ),
        migrations.AlterField(
            model_name='postuploaddetails',
            name='updatedDate',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 12, 16, 19, 19, 30313), verbose_name='Post Last Updated At'),
        ),
        migrations.AlterField(
            model_name='user',
            name='createdDate',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 12, 16, 19, 19, 19379), verbose_name='User Created At'),
        ),
        migrations.AlterField(
            model_name='user',
            name='lastlogin',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 12, 16, 19, 19, 19406), verbose_name='User Last LoggedIn At'),
        ),
        migrations.AlterField(
            model_name='user',
            name='updatedDate',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 12, 16, 19, 19, 19388), verbose_name='User Last Updated At'),
        ),
    ]
