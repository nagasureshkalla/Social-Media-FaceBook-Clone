# Generated by Django 4.0.4 on 2022-06-12 15:25

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor',
            name='userId',
            field=models.CharField(default='0', max_length=100),
        ),
        migrations.AlterField(
            model_name='clinic',
            name='createdDate',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 12, 15, 25, 2, 175312), verbose_name='Clinic created At'),
        ),
        migrations.AlterField(
            model_name='clinic',
            name='updatedDate',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 12, 15, 25, 2, 175321), verbose_name='Clinic Last Updated At'),
        ),
        migrations.AlterField(
            model_name='doctor',
            name='createdDate',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 12, 15, 25, 2, 175794), verbose_name='Clinic created At'),
        ),
        migrations.AlterField(
            model_name='doctor',
            name='updatedDate',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 12, 15, 25, 2, 175802), verbose_name='Clinic Last Updated At'),
        ),
        migrations.AlterField(
            model_name='doctorbooking',
            name='createdDate',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 12, 15, 25, 2, 176275), verbose_name='Slot created At'),
        ),
        migrations.AlterField(
            model_name='doctorbooking',
            name='updatedDate',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 12, 15, 25, 2, 176284), verbose_name='Slot Last Updated At'),
        ),
        migrations.AlterField(
            model_name='messages',
            name='createdDate',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 12, 15, 25, 2, 171323), verbose_name='Chat Last created At'),
        ),
        migrations.AlterField(
            model_name='messages',
            name='updatedDate',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 12, 15, 25, 2, 171335), verbose_name='Chat Last updated At'),
        ),
        migrations.AlterField(
            model_name='post',
            name='createdDate',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 12, 15, 25, 2, 169690), verbose_name='Post Last created At'),
        ),
        migrations.AlterField(
            model_name='post',
            name='updatedDate',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 12, 15, 25, 2, 169702), verbose_name='Post Last Updated At'),
        ),
        migrations.AlterField(
            model_name='postuploaddetails',
            name='createdDate',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 12, 15, 25, 2, 170162), verbose_name='Post Last created At'),
        ),
        migrations.AlterField(
            model_name='postuploaddetails',
            name='updatedDate',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 12, 15, 25, 2, 170171), verbose_name='Post Last Updated At'),
        ),
        migrations.AlterField(
            model_name='user',
            name='createdDate',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 12, 15, 25, 2, 153723), verbose_name='User Created At'),
        ),
        migrations.AlterField(
            model_name='user',
            name='lastlogin',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 12, 15, 25, 2, 153752), verbose_name='User Last LoggedIn At'),
        ),
        migrations.AlterField(
            model_name='user',
            name='updatedDate',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 12, 15, 25, 2, 153732), verbose_name='User Last Updated At'),
        ),
    ]
