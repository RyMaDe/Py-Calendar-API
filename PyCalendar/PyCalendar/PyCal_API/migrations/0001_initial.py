# Generated by Django 4.0.4 on 2022-05-29 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Calendar_API',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=50)),
                ('Description', models.TextField(blank=True)),
                ('Date', models.DateField()),
                ('Time', models.TimeField(blank=True, null=True)),
                ('Tag', models.CharField(blank=True, choices=[('Work', 'Work'), ('Fun', 'Fun')], max_length=5)),
            ],
        ),
    ]
