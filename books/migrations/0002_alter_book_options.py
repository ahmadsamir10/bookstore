# Generated by Django 5.0 on 2024-11-22 02:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='book',
            options={'ordering': ['-published_date'], 'verbose_name': 'Book', 'verbose_name_plural': 'Books'},
        ),
    ]
