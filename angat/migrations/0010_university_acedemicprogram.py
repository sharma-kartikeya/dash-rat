# Generated by Django 4.2.16 on 2024-10-30 14:49

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('angat', '0009_rename_bachlors_degree_gloverauser_bachlors_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='University',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=512)),
                ('type', models.CharField(choices=[('private', 'Private'), ('public', 'Public')], default='private', max_length=255)),
                ('location', models.CharField(max_length=255)),
                ('location_details', models.TextField(blank=True, null=True)),
                ('usp', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='AcedemicProgram',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('ranking', models.CharField(blank=True, max_length=255, null=True)),
                ('college', models.CharField(max_length=512)),
                ('name', models.CharField(max_length=512)),
                ('usp', models.TextField(blank=True, null=True)),
                ('specialization', models.TextField(blank=True, null=True)),
                ('intern_or_co_op', models.CharField(blank=True, max_length=100, null=True)),
                ('curriculum_link', models.URLField(blank=True, max_length=100, null=True)),
                ('cost', models.JSONField()),
                ('credits', models.JSONField()),
                ('eligibility', models.JSONField()),
                ('application_requirements', models.JSONField()),
                ('placement_details', models.JSONField()),
                ('study_type', models.CharField(max_length=100)),
                ('university', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='angat.university')),
            ],
        ),
    ]
