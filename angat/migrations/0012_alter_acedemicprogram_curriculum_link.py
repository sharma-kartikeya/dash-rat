# Generated by Django 4.2.16 on 2024-10-30 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('angat', '0011_alter_acedemicprogram_curriculum_link_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='acedemicprogram',
            name='curriculum_link',
            field=models.URLField(blank=True, max_length=512, null=True),
        ),
    ]
