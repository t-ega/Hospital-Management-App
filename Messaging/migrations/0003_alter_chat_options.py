# Generated by Django 4.1.7 on 2023-02-24 01:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Messaging', '0002_alter_chat_messages'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='chat',
            options={'get_latest_by': 'timestamp'},
        ),
    ]
