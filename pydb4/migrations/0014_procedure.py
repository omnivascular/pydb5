# Generated by Django 4.2.1 on 2023-06-29 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pydb4', '0013_alter_auditlog_omni_employee'),
    ]

    operations = [
        migrations.CreateModel(
            name='Procedure',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('procedure', models.CharField(max_length=300)),
                ('patient', models.CharField(max_length=300)),
                ('date_performed', models.DateTimeField(auto_now=True)),
                ('products_used', models.ManyToManyField(to='pydb4.product')),
            ],
        ),
    ]
