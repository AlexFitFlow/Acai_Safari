# Generated by Django 2.2 on 2022-02-05 00:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Acai_App', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Acai',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('method', models.CharField(max_length=255)),
                ('size', models.CharField(max_length=255)),
                ('base', models.CharField(max_length=255)),
                ('quantity', models.IntegerField(max_length=255)),
                ('toppings', models.CharField(max_length=255)),
            ],
        ),
    ]
