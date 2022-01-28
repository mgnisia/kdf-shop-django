# Generated by Django 4.0.1 on 2022-01-28 21:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_remove_order_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='items_ordered',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='order',
            name='paid',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='order',
            name='post_delivery',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='order',
            name='email',
            field=models.EmailField(max_length=100),
        ),
    ]