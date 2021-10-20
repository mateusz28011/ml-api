# Generated by Django 3.2.8 on 2021-10-20 09:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ml', '0002_auto_20211019_2149'),
    ]

    operations = [
        migrations.CreateModel(
            name='KmeansParameters',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('n_clusters', models.PositiveSmallIntegerField(default=8)),
                ('init', models.PositiveSmallIntegerField(choices=[(0, 'k-means++'), (1, 'random')], default=0)),
                ('n_init', models.PositiveSmallIntegerField(default=10)),
                ('max_iter', models.PositiveSmallIntegerField(default=300)),
                ('algorithm', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='ml.algorithm')),
            ],
        ),
    ]
