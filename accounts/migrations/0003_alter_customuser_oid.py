# Generated by Django 4.2.9 on 2024-01-23 09:15

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0002_alter_customuser_oid"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="oid",
            field=models.BigIntegerField(null=True, unique=True),
        ),
    ]
