# Generated by Django 4.2.7 on 2024-01-23 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100, verbose_name='이름')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='이메일')),
                ('password', models.CharField(max_length=300, verbose_name='비밀번호')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='등록일')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='수정일')),
            ],
        ),
    ]
