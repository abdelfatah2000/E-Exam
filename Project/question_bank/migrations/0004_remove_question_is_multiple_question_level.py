# Generated by Django 4.0.4 on 2022-05-20 00:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('question_bank', '0003_alter_question_professor'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='is_multiple',
        ),
        migrations.AddField(
            model_name='question',
            name='level',
            field=models.CharField(choices=[('F', 'One'), ('S', 'Two'), ('T', 'Three')], default='S', max_length=1),
        ),
    ]
