# Generated by Django 4.1.2 on 2022-11-25 00:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Striker', '0019_alter_toon_forcealignment'),
    ]

    operations = [
        migrations.AddField(
            model_name='toon',
            name='crew1',
            field=models.CharField(blank=True, max_length=45),
        ),
        migrations.AddField(
            model_name='toon',
            name='crew2',
            field=models.CharField(blank=True, max_length=45),
        ),
        migrations.AddField(
            model_name='toon',
            name='crew3',
            field=models.CharField(blank=True, max_length=45),
        ),
    ]
