# Generated by Django 4.2.7 on 2024-03-27 02:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('intro', '0007_alter_contact_map_add'),
    ]

    operations = [
        migrations.CreateModel(
            name='Intro',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='제목')),
                ('contents', models.TextField(max_length=3000, verbose_name='내용')),
                ('image', models.ImageField(blank=True, null=True, upload_to='intro/intro/img/', verbose_name='이미지')),
            ],
            options={
                'verbose_name': '인사말',
                'verbose_name_plural': '인사말',
                'db_table': 'intro_Intro',
            },
        ),
    ]
