# Generated by Django 3.2.3 on 2021-07-28 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_message_isreaded'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]
