# Generated by Django 2.1.2 on 2018-10-20 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='cache',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='contestant',
            name='username',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]
