# Generated by Django 4.0.4 on 2022-05-21 22:45

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_alter_professor_student_student'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='score',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]
