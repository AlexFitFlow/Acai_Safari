# Generated by Django 2.2 on 2022-02-05 23:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Acai_App', '0002_acai'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=6)),
                ('acai', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='acai_orders', to='Acai_App.Acai')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='Acai_App.User')),
            ],
        ),
    ]
