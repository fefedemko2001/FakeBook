# Generated by Django 5.0.1 on 2024-07-31 09:42

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('friends', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='friendship',
            unique_together=set(),
        ),
        migrations.AddConstraint(
            model_name='friendship',
            constraint=models.UniqueConstraint(condition=models.Q(('user1__gt', models.F('user2')), _negated=True), fields=('user1', 'user2'), name='unique_friendship_pair'),
        ),
        migrations.AddConstraint(
            model_name='friendship',
            constraint=models.UniqueConstraint(condition=models.Q(('user2__gt', models.F('user1')), _negated=True), fields=('user2', 'user1'), name='unique_reverse_friendship_pair'),
        ),
    ]
