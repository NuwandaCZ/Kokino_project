# Generated by Django 3.0.7 on 2020-09-10 20:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('toilet', '0007_auto_20200910_2149'),
    ]

    operations = [
        migrations.AddField(
            model_name='toilet',
            name='rating',
            field=models.FloatField(default=0.0),
        ),
    ]
