# Generated by Django 5.1.2 on 2024-10-26 21:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_rename_notification_notifications'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notify',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sender', models.CharField(max_length=250)),
                ('body', models.CharField(max_length=250)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
