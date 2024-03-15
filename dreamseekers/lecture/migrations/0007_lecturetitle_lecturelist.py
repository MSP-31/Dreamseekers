# Generated by Django 4.2.7 on 2024-03-14 13:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lecture', '0006_rename_end_time_lecturecalender_endtime_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='lectureTitle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='제목')),
                ('image', models.ImageField(blank=True, null=True, upload_to='lecture/list/img/', verbose_name='이미지')),
            ],
            options={
                'verbose_name': '강의제목',
                'verbose_name_plural': '강의제목',
                'db_table': 'lecture_title',
            },
        ),
        migrations.CreateModel(
            name='lectureList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='제목')),
                ('content', models.TextField(verbose_name='내용')),
                ('lecture_list', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lecture.lecturetitle', verbose_name='강의리스트')),
            ],
            options={
                'verbose_name': '강의리스트',
                'verbose_name_plural': '강의리스트',
                'db_table': 'lecture_list',
            },
        ),
    ]
