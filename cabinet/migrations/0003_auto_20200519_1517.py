# Generated by Django 3.0.2 on 2020-05-19 12:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cabinet', '0002_post'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'verbose_name': 'Пост', 'verbose_name_plural': 'Посты'},
        ),
    ]