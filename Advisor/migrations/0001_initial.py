# Generated by Django 2.2.5 on 2020-04-03 12:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='Class',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('section', models.CharField(max_length=4)),
                ('batch', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('HOD', models.CharField(blank=True, default=None, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='teachers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=100)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=1)),
                ('email', models.EmailField(max_length=255)),
                ('contact', models.CharField(max_length=50)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Advisor.department')),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(max_length=50, unique=True)),
                ('admin', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('teacher', models.OneToOneField(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='Advisor.teachers')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'permissions': [('can_upload_students', 'Can upload student data'), ('can_assign_mentors', 'Can assign mentors to class')],
            },
        ),
        migrations.CreateModel(
            name='students',
            fields=[
                ('urn', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('crn', models.PositiveIntegerField()),
                ('photo', models.ImageField(default=None, null=True, upload_to='students')),
                ('full_name', models.CharField(max_length=255)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=1)),
                ('dob', models.DateField()),
                ('blood_group', models.CharField(max_length=4)),
                ('category', models.CharField(max_length=255)),
                ('height', models.PositiveIntegerField()),
                ('weight', models.PositiveIntegerField()),
                ('living', models.CharField(choices=[('DAY SCHOLAR', 'DAY SCHOLAR'), ('HOSTELLER', 'HOSTELLER')], max_length=12)),
                ('Father_pic', models.ImageField(default=None, null=True, upload_to='father')),
                ('Father_name', models.CharField(max_length=255)),
                ('Father_contact', models.CharField(max_length=15)),
                ('Mother_pic', models.ImageField(default=None, null=True, upload_to='mother')),
                ('Mother_name', models.CharField(max_length=255)),
                ('Mother_contact', models.CharField(max_length=15)),
                ('Address', models.CharField(max_length=255)),
                ('City', models.CharField(max_length=255)),
                ('State', models.CharField(max_length=255)),
                ('District', models.CharField(max_length=255)),
                ('Pincode', models.PositiveIntegerField()),
                ('Contact', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=254)),
                ('Class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Advisor.Class')),
            ],
        ),
        migrations.CreateModel(
            name='marks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sgpa', models.PositiveIntegerField()),
                ('active_backs', models.PositiveIntegerField()),
                ('passive_backs', models.PositiveIntegerField()),
                ('sem', models.PositiveIntegerField()),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Advisor.students')),
            ],
        ),
        migrations.AddField(
            model_name='class',
            name='Mentor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Advisor.teachers'),
        ),
        migrations.AddField(
            model_name='class',
            name='department',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Advisor.department'),
        ),
    ]
