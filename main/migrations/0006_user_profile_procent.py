# Generated by Django 3.2.3 on 2021-07-11 21:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_alter_chat_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_profile',
            name='procent',
            field=models.FloatField(default=0.0),
        ),
    ]