# Generated by Django 4.2.5 on 2023-10-14 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0013_package_seats'),
    ]

    operations = [
        migrations.AddField(
            model_name='package',
            name='desc',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
