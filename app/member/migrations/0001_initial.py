# Generated by Django 3.1.2 on 2020-10-10 17:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullname', models.CharField(max_length=100)),
                ('id_doc', models.CharField(max_length=50, unique=True)),
                ('birthdate', models.DateField()),
                ('sex', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], max_length=1)),
                ('monthly_payment', models.DecimalField(decimal_places=2, max_digits=8)),
                ('active', models.BooleanField(default=True)),
                ('register_date', models.DateField(auto_now_add=True)),
                ('departure_date', models.DateField(default=None, null=True)),
                ('email', models.EmailField(max_length=254)),
                ('phone_number', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('member_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='member.member')),
                ('scholar_year', models.PositiveSmallIntegerField()),
                ('guardian1', models.CharField(max_length=100)),
                ('guardian2', models.CharField(blank=True, max_length=100)),
            ],
            bases=('member.member',),
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('member_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='member.member')),
                ('academic_level', models.CharField(choices=[('Gr', 'Graduate'), ('Ms', 'Master'), ('Dr', 'Docter')], max_length=2)),
                ('bank_agency', models.PositiveIntegerField()),
                ('bank_account', models.PositiveIntegerField()),
            ],
            bases=('member.member',),
        ),
    ]
