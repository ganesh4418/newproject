# Generated by Django 4.2.6 on 2023-10-16 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('intel', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactUs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Full_name', models.CharField(max_length=100)),
                ('Company', models.CharField(max_length=100)),
                ('Business_email', models.EmailField(max_length=254)),
                ('Contact_number', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='HelpandSupport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Full_name', models.CharField(max_length=100)),
                ('Company', models.CharField(max_length=100)),
                ('Business_email', models.EmailField(max_length=254)),
                ('Contact_number', models.CharField(max_length=20)),
            ],
        ),
    ]
