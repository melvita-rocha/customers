# Generated by Django 4.2.5 on 2023-09-21 09:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='DataSheet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=50)),
                ('historical_data', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Profession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('doc_type', models.CharField(choices=[('PP', 'Passport'), ('ID', 'Identity card'), ('OT', 'Others')], max_length=10)),
                ('doc_number', models.CharField(max_length=50)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.customer')),
            ],
        ),
        migrations.AddField(
            model_name='customer',
            name='data_sheet',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='core.datasheet'),
        ),
        migrations.AddField(
            model_name='customer',
            name='professions',
            field=models.ManyToManyField(to='core.profession'),
        ),
    ]
