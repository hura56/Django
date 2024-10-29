# Generated by Django 5.0 on 2024-01-16 22:59

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('event', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Fighter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('age', models.IntegerField(null=True)),
                ('record', models.CharField(default='0:0', max_length=10)),
                ('rank', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='WeightClass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Default', max_length=100)),
                ('weight', models.FloatField(default=500)),
            ],
        ),
        migrations.CreateModel(
            name='Fight',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='event.event')),
                ('fighter1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fighter1', to='fight.fighter')),
                ('fighter2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fighter2', to='fight.fighter')),
                ('winner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='winner', to='fight.fighter')),
                ('weight_class', models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='fight.weightclass')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('date_added', models.DateField(auto_now=True)),
                ('user_added', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('fight', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='fight.fight')),
            ],
        ),
        migrations.CreateModel(
            name='FavouriteFighter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('fighter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fight.fighter')),
            ],
        ),
        migrations.CreateModel(
            name='Prediction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fight', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fight.fight')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('winner_prediction', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='fight.fighter')),
            ],
        ),
        migrations.AddField(
            model_name='fighter',
            name='weight_class',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='fight.weightclass'),
        ),
    ]