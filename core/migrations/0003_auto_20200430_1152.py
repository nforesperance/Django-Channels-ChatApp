# Generated by Django 3.0.5 on 2020-04-30 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_group'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='messages',
            field=models.TextField(default=[]),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='group',
            name='members',
            field=models.TextField(),
        ),
    ]
