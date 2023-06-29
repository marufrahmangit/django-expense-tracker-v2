# Generated by Django 4.2.2 on 2023-06-22 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.RemoveField(
            model_name='expense',
            name='item_name',
        ),
        migrations.AddField(
            model_name='expense',
            name='items',
            field=models.ManyToManyField(to='app.item'),
        ),
    ]