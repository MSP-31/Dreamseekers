# Generated by Django 4.2.7 on 2024-04-03 02:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notice', '0002_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='notice',
            options={'verbose_name': '공지사항', 'verbose_name_plural': '공지사항'},
        ),
    ]
