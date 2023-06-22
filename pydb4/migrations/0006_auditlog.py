# Generated by Django 4.2.1 on 2023-06-19 15:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('pydb4', '0005_product_audit_log_alter_product_barcode'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuditLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('field_name', models.CharField(max_length=255)),
                ('old_value', models.CharField(max_length=255)),
                ('new_value', models.CharField(max_length=255)),
                ('modified_date', models.DateTimeField()),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
            ],
        ),
    ]
