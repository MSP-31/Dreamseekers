# Generated by Django 4.2.7 on 2024-04-03 02:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lecture', '0012_lecturelist_contents_lecturelist_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lecturelist',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='lecture/list/detail/img/', verbose_name='이미지'),
        ),
    ]
