# Generated by Django 4.2.7 on 2024-05-29 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lecture', '0013_alter_lecturelist_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inquiry',
            name='phone',
            field=models.CharField(max_length=45, verbose_name='연락처'),
        ),
    ]
