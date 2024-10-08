# Generated by Django 4.2.5 on 2023-10-06 11:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0005_alter_users_phone_busdetails'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='busdetails',
            name='link',
        ),
        migrations.RemoveField(
            model_name='busdetails',
            name='name',
        ),
        migrations.RemoveField(
            model_name='busdetails',
            name='phone',
        ),
        migrations.CreateModel(
            name='Hoteldetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_no', models.CharField(max_length=100, null=True)),
                ('room_desc', models.CharField(max_length=100, null=True)),
                ('busprofile', models.FileField(null=True, upload_to='')),
                ('owner_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
