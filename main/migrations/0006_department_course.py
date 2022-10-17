# Generated by Django 4.1.1 on 2022-10-17 19:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_delete_department'),
    ]

    operations = [
        migrations.CreateModel(
            name='department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('abbreviation', models.CharField(max_length=10)),
                ('departmentName', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('courseNumber', models.IntegerField()),
                ('description', models.CharField(max_length=70)),
                ('instructorName', models.CharField(max_length=30)),
                ('instructorEmail', models.EmailField(max_length=20)),
                ('semesterCode', models.IntegerField()),
                ('courseSection', models.CharField(max_length=5)),
                ('credits', models.CharField(max_length=2)),
                ('lectureType', models.CharField(max_length=5)),
                ('classCapacity', models.IntegerField()),
                ('classEnrollment', models.IntegerField()),
                ('classSpotsOpen', models.IntegerField()),
                ('waitlist', models.IntegerField()),
                ('waitlistMax', models.IntegerField()),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.department')),
            ],
        ),
    ]
