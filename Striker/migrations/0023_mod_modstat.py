# Generated by Django 3.2 on 2022-11-26 16:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Striker', '0022_remove_toon_crewone_remove_toon_crewthree_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modId', models.CharField(max_length=30)),
                ('modLevel', models.SmallIntegerField()),
                ('tier', models.SmallIntegerField()),
                ('set', models.SmallIntegerField()),
                ('pips', models.SmallIntegerField()),
                ('toon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Striker.toon')),
            ],
        ),
        migrations.CreateModel(
            name='ModStat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('statType', models.CharField(default='P', max_length=1)),
                ('unitStat', models.CharField(default='', max_length=30)),
                ('value', models.DecimalField(decimal_places=5, max_digits=10)),
                ('roll', models.SmallIntegerField(default=0)),
                ('mod', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Striker.mod')),
            ],
        ),
    ]
