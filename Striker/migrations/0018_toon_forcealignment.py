# Generated by Django 4.1.2 on 2022-11-24 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Striker', '0017_alter_toon_iszeta'),
    ]

    operations = [
        migrations.AddField(
            model_name='toon',
            name='forceAlignment',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]
