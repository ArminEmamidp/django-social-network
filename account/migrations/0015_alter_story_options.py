# Generated by Django 4.2.6 on 2023-12-02 14:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0014_music'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='story',
            options={'ordering': ['-created']},
        ),
    ]
