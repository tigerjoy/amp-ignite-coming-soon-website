# Generated by Django 4.2.10 on 2024-02-25 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coming_soon_website', '0006_contactformdata_contact_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactformdata',
            name='email_message_id',
            field=models.TextField(blank=True, null=True),
        ),
    ]