# Generated by Django 2.2.27 on 2023-03-22 09:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('student_management_app', '0006_studentresult_balance'),
    ]

    operations = [
        migrations.AddField(
            model_name='students',
            name='balance',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8),
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=8)),
                ('transaction_id', models.CharField(max_length=255)),
                ('payment_date', models.DateTimeField(auto_now_add=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student_management_app.Students')),
            ],
        ),
    ]