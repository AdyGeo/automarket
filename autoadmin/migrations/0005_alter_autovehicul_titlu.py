# Generated by Django 4.1.3 on 2023-01-15 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autoadmin', '0004_alter_cutiedeviteza_options_alter_dotare_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='autovehicul',
            name='titlu',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]