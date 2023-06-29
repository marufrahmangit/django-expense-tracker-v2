# Generated by Django 4.2.2 on 2023-06-22 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_alter_item_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='expense',
            name='entry_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='expense',
            name='last_update_date',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='expensemethod',
            name='entry_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='expensemethod',
            name='last_update_date',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='item',
            name='entry_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='item',
            name='last_update_date',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]