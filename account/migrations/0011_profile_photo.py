# Generated by Django 3.2.23 on 2023-12-03 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0010_remove_profile_gender_remove_profile_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='photo',
            field=models.ImageField(default=1, upload_to='users/'),
            preserve_default=False,
        ),
    ]
