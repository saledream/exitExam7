# Generated by Django 5.0.3 on 2024-03-30 05:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('instructor', '0017_testquestion_question_type'),
    ]

    operations = [
        migrations.RenameField(
            model_name='examstatus',
            old_name='question_catefory',
            new_name='question_category',
        ),
    ]