# Generated by Django 4.2.10 on 2024-02-25 13:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('coming_soon_website', '0009_apicallerrorlog_contact_form_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='apicallerrorlog',
            name='error_type',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='apicallerrorlog',
            name='contact_form_data',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='coming_soon_website.contactformdata'),
        ),
        migrations.DeleteModel(
            name='ApiTokenRefreshErrorLog',
        ),
    ]
