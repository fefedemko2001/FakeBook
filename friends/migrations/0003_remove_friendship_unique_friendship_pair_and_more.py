# Generated by Django 5.0.1 on 2024-07-31 09:47

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('friends', '0002_alter_friendship_unique_together_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='friendship',
            name='unique_friendship_pair',
        ),
        migrations.RemoveConstraint(
            model_name='friendship',
            name='unique_reverse_friendship_pair',
        ),
        migrations.AddConstraint(
            model_name='friendship',
            constraint=models.UniqueConstraint(fields=('user1', 'user2'), name='unique_friendship_pair'),
        ),
    ]
