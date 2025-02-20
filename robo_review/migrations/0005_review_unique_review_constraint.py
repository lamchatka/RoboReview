# Generated by Django 5.1.4 on 2025-02-20 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('robo_review', '0004_review_review_date'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='review',
            constraint=models.UniqueConstraint(fields=('book', 'author_nickname', 'text', 'source'), name='unique_review_constraint'),
        ),
    ]
