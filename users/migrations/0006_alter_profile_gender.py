# Generated by Django 5.0.1 on 2024-09-30 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_remove_profile_first_name_remove_profile_last_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='gender',
            field=models.CharField(blank=True, choices=[('man', 'Man'), ('woman', 'Woman'), ('other', 'Other')], max_length=10, null=True),
        ),
    ]
