# Generated by Django 5.0.1 on 2024-07-31 11:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_alter_message_body'),
        ('users', '0005_remove_profile_first_name_remove_profile_last_name'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Message',
            new_name='ChatMessage',
        ),
    ]
