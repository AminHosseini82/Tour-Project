# Generated by Django 5.1.6 on 2025-03-02 20:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='phone_number',
            field=models.CharField(default=1, max_length=15, unique=True),
            preserve_default=False,
        ),
    ]
