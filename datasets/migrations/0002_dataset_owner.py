# Generated by Django 3.2.8 on 2021-10-14 12:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('datasets', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='dataset',
            name='owner',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.PROTECT, related_name='owner', to='auth.user'),
            preserve_default=False,
        ),
    ]