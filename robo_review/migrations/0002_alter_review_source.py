# Generated by Django 5.1.4 on 2025-02-25 20:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('robo_review', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='source',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='robo_review.source'),
        ),
    ]
