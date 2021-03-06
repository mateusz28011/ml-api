# Generated by Django 3.2.8 on 2021-10-26 13:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ml', '0006_auto_20211025_1957'),
    ]

    operations = [
        migrations.CreateModel(
            name='Scores',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('silhouette_score', models.FloatField()),
                ('calinski_harabasz_score', models.FloatField()),
                ('davies_bouldin_score', models.FloatField()),
                ('algorithm_data', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='ml.algorithmdata')),
            ],
        ),
    ]
