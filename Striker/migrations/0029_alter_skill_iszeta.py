# Generated by Django 4.1.2 on 2022-12-12 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Striker', '0028_alter_toon_combattype'),
    ]

    operations = [
        migrations.AlterField(
            model_name='skill',
            name='isZeta',
            field=models.CharField(blank=True, max_length=45),
        ),
    ]
