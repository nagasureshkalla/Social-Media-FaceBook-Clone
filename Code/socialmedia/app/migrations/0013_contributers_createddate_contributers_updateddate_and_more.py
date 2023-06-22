# Generated by Django 4.0.4 on 2022-06-17 22:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_payment_refundstatus_alter_clinic_createddate_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='contributers',
            name='createdDate',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 17, 22, 14, 31, 225397), verbose_name='Contributer created At'),
        ),
        migrations.AddField(
            model_name='contributers',
            name='updatedDate',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 17, 22, 14, 31, 225405), verbose_name='Contributer Last Updated At'),
        ),
        migrations.AddField(
            model_name='followers',
            name='createdDate',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 17, 22, 14, 31, 225210), verbose_name='Follower created At'),
        ),
        migrations.AddField(
            model_name='followers',
            name='updatedDate',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 17, 22, 14, 31, 225217), verbose_name='Follower Last Updated At'),
        ),
        migrations.AddField(
            model_name='likes',
            name='createdDate',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 17, 22, 14, 31, 226881), verbose_name='Like created At'),
        ),
        migrations.AddField(
            model_name='likes',
            name='updatedDate',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 17, 22, 14, 31, 226888), verbose_name='Like Last Updated At'),
        ),
        migrations.AlterField(
            model_name='clinic',
            name='createdDate',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 17, 22, 14, 31, 228200), verbose_name='Clinic created At'),
        ),
        migrations.AlterField(
            model_name='clinic',
            name='updatedDate',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 17, 22, 14, 31, 228207), verbose_name='Clinic Last Updated At'),
        ),
        migrations.AlterField(
            model_name='doctor',
            name='createdDate',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 17, 22, 14, 31, 228520), verbose_name='Clinic created At'),
        ),
        migrations.AlterField(
            model_name='doctor',
            name='updatedDate',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 17, 22, 14, 31, 228528), verbose_name='Clinic Last Updated At'),
        ),
        migrations.AlterField(
            model_name='doctorbooking',
            name='createdDate',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 17, 22, 14, 31, 228918), verbose_name='Slot created At'),
        ),
        migrations.AlterField(
            model_name='doctorbooking',
            name='updatedDate',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 17, 22, 14, 31, 228925), verbose_name='Slot Last Updated At'),
        ),
        migrations.AlterField(
            model_name='messages',
            name='createdDate',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 17, 22, 14, 31, 225662), verbose_name='Chat Last created At'),
        ),
        migrations.AlterField(
            model_name='messages',
            name='updatedDate',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 17, 22, 14, 31, 225669), verbose_name='Chat Last updated At'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='createdDate',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 17, 22, 14, 31, 273738), verbose_name='Payment Last created At'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='updatedDate',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 17, 22, 14, 31, 273750), verbose_name='Payment Last updated At'),
        ),
        migrations.AlterField(
            model_name='post',
            name='createdDate',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 17, 22, 14, 31, 218480), verbose_name='Post Last created At'),
        ),
        migrations.AlterField(
            model_name='post',
            name='updatedDate',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 17, 22, 14, 31, 218491), verbose_name='Post Last Updated At'),
        ),
        migrations.AlterField(
            model_name='postuploaddetails',
            name='createdDate',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 17, 22, 14, 31, 224853), verbose_name='Post Last created At'),
        ),
        migrations.AlterField(
            model_name='postuploaddetails',
            name='updatedDate',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 17, 22, 14, 31, 224865), verbose_name='Post Last Updated At'),
        ),
        migrations.AlterField(
            model_name='user',
            name='createdDate',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 17, 22, 14, 31, 209524), verbose_name='User Created At'),
        ),
        migrations.AlterField(
            model_name='user',
            name='lastlogin',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 17, 22, 14, 31, 209551), verbose_name='User Last LoggedIn At'),
        ),
        migrations.AlterField(
            model_name='user',
            name='updatedDate',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 17, 22, 14, 31, 209534), verbose_name='User Last Updated At'),
        ),
    ]