# Generated by Django 4.1.5 on 2023-01-15 20:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clothes_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Institution',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('description', models.TextField(blank=True, null=True)),
                ('type', models.IntegerField(choices=[(1, 'Fundacja'), (2, 'Organizacja pozarządowa'), (3, 'Zbiórka lokalna')], default=1)),
                ('categories', models.ManyToManyField(to='clothes_app.category')),
            ],
        ),
    ]
