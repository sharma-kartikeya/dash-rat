# Generated by Django 4.2.16 on 2024-10-18 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('angat', '0005_remove_usermessage_message_ptr_message_context_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='role_type',
            field=models.CharField(choices=[('user', 'User'), ('assistant', 'Assistant')], max_length=10),
        ),
    ]
