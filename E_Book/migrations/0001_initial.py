# Generated by Django 5.0.7 on 2024-10-24 08:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book_name', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('date_of_upload', models.DateField(auto_now_add=True)),
                ('file', models.FileField(upload_to='book')),
            ],
        ),
        migrations.CreateModel(
            name='Login',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=50)),
                ('type', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('dob', models.DateField()),
                ('phone', models.BigIntegerField()),
                ('email', models.CharField(max_length=50)),
                ('photo', models.FileField(upload_to='')),
                ('place', models.CharField(max_length=50)),
                ('pin', models.BigIntegerField()),
                ('post', models.CharField(max_length=100)),
                ('gender', models.CharField(max_length=15)),
                ('LOGIN', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='E_Book.login')),
            ],
        ),
        migrations.CreateModel(
            name='Feedbacks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feedback', models.TextField()),
                ('rating', models.IntegerField()),
                ('date', models.DateField()),
                ('BOOK', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='E_Book.book')),
                ('USER', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='E_Book.user')),
            ],
        ),
        migrations.CreateModel(
            name='Complaint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('complaint', models.TextField()),
                ('content', models.TextField()),
                ('date', models.DateField()),
                ('reply', models.TextField(default='pending')),
                ('USER', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='E_Book.user')),
            ],
        ),
        migrations.CreateModel(
            name='BookEditRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(default='pending', max_length=30)),
                ('date', models.DateField(auto_now_add=True)),
                ('BOOK', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='E_Book.book')),
                ('USER', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='E_Book.user')),
            ],
        ),
        migrations.AddField(
            model_name='book',
            name='USER',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='E_Book.user'),
        ),
    ]
