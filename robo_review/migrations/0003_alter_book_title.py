# Generated by Django 5.1.4 on 2025-02-19 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('robo_review', '0002_remove_review_user_review_author_nickname_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='title',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
