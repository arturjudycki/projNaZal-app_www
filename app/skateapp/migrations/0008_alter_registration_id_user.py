# Generated by Django 4.1.4 on 2022-12-13 14:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('skateapp', '0007_alter_registration_id_competition'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registration',
            name='id_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='registration', to=settings.AUTH_USER_MODEL),
        ),
    ]
