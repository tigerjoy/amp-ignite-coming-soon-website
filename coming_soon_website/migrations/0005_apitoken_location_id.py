# Generated by Django 4.2.10 on 2024-02-25 04:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coming_soon_website', '0004_apitoken_created_at_apitoken_modified_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='apitoken',
            name='location_id',
            field=models.TextField(default='UzCqsTe4vdxvfHHuhi9E'),
            preserve_default=False,
        ),
    ]