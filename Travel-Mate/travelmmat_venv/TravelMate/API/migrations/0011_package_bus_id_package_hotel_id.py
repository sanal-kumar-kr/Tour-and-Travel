# Generated by Django 4.2.5 on 2023-10-11 09:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0010_package'),
    ]

    operations = [
        migrations.AddField(
            model_name='package',
            name='bus_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='API.busdetails'),
        ),
        migrations.AddField(
            model_name='package',
            name='hotel_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
