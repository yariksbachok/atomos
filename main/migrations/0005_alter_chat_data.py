# Generated by Django 3.2.3 on 2021-07-02 15:42

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_chat_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chat',
            name='data',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]