# Generated by Django 4.0.4 on 2022-05-24 20:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0010_alter_user_role'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProfessorProxy',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('user.professor',),
        ),
    ]
