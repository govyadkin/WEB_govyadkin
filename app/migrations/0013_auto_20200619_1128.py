# Generated by Django 3.0.4 on 2020-06-19 11:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_auto_20200619_1116'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='asking',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='asking', to='app.myUser'),
        ),
    ]
