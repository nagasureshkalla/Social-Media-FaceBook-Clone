# Generated by Django 4.0.4 on 2022-06-13 23:38

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_alter_clinic_createddate_alter_clinic_updateddate_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctorbooking',
            name='appointmentstatus',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='clinic',
            name='createdDate',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 13, 23, 38, 53, 715469), verbose_name='Clinic created At'),
        ),
        migrations.AlterField(
            model_name='clinic',
            name='updatedDate',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 13, 23, 38, 53, 715478), verbose_name='Clinic Last Updated At'),
        ),
        migrations.AlterField(
            model_name='doctor',
            name='createdDate',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 13, 23, 38, 53, 715834), verbose_name='Clinic created At'),
        ),
        migrations.AlterField(
            model_name='doctor',
            name='updatedDate',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 13, 23, 38, 53, 715842), verbose_name='Clinic Last Updated At'),
        ),
        migrations.AlterField(
            model_name='doctorbooking',
            name='createdDate',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 13, 23, 38, 53, 716184), verbose_name='Slot created At'),
        ),
        migrations.AlterField(
            model_name='doctorbooking',
            name='updatedDate',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 13, 23, 38, 53, 716192), verbose_name='Slot Last Updated At'),
        ),
        migrations.AlterField(
            model_name='messages',
            name='createdDate',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 13, 23, 38, 53, 713079), verbose_name='Chat Last created At'),
        ),
        migrations.AlterField(
            model_name='messages',
            name='updatedDate',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 13, 23, 38, 53, 713088), verbose_name='Chat Last updated At'),
        ),
        migrations.AlterField(
            model_name='post',
            name='createdDate',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 13, 23, 38, 53, 712149), verbose_name='Post Last created At'),
        ),
        migrations.AlterField(
            model_name='post',
            name='updatedDate',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 13, 23, 38, 53, 712160), verbose_name='Post Last Updated At'),
        ),
        migrations.AlterField(
            model_name='postuploaddetails',
            name='createdDate',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 13, 23, 38, 53, 712454), verbose_name='Post Last created At'),
        ),
        migrations.AlterField(
            model_name='postuploaddetails',
            name='updatedDate',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 13, 23, 38, 53, 712461), verbose_name='Post Last Updated At'),
        ),
        migrations.AlterField(
            model_name='user',
            name='createdDate',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 13, 23, 38, 53, 701870), verbose_name='User Created At'),
        ),
        migrations.AlterField(
            model_name='user',
            name='lastlogin',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 13, 23, 38, 53, 701898), verbose_name='User Last LoggedIn At'),
        ),
        migrations.AlterField(
            model_name='user',
            name='updatedDate',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 13, 23, 38, 53, 701878), verbose_name='User Last Updated At'),
        ),
    ]
