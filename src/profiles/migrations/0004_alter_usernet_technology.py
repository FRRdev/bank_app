# Generated by Django 3.2.9 on 2021-12-13 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_auto_20211201_1255'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usernet',
            name='technology',
            field=models.ManyToManyField(blank=True, null=True, related_name='users', to='profiles.Technology'),
        ),
    ]
