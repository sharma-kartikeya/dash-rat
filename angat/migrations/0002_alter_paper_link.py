# Generated by Django 4.2.16 on 2024-10-15 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('angat', '0001_pg_vector_extenstion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paper',
            name='link',
            field=models.URLField(blank=True, max_length=100, null=True),
        ),
    ]
