# Generated by Django 5.0 on 2024-01-10 16:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='WeightClass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('weight', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Fighter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('age', models.IntegerField(null=True)),
                ('record', models.CharField(default='0:0', max_length=10)),
                ('rank', models.IntegerField(null=True)),
                ('weight_class', models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='MMA.weightclass')),
            ],
        ),
        migrations.CreateModel(
            name='fight',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MMA.event')),
                ('fighter1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fighter1', to='MMA.fighter')),
                ('fighter2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fighter2', to='MMA.fighter')),
                ('winner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='winner', to='MMA.fighter')),
                ('weight_class', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='MMA.weightclass')),
            ],
        ),
    ]
