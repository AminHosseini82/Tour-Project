# Generated by Django 5.1.4 on 2024-12-25 10:50

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_news', models.CharField(blank=True, max_length=50, null=True, verbose_name='Title')),
                ('description_news', models.CharField(blank=True, max_length=200, null=True)),
                ('image_news', models.ImageField(blank=True, null=True, upload_to='tourr/')),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_news', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
