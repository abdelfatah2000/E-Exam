# Generated by Django 4.0.4 on 2022-05-20 22:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_alter_group_level'),
        ('exam', '0003_alter_examgroups_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='examgroups',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='user.group'),
        ),
    ]
