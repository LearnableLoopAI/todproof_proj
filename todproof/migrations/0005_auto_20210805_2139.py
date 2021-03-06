# Generated by Django 3.2.5 on 2021-08-05 21:39

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('todproof', '0004_auto_20210805_2107'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contribution',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kind', models.CharField(choices=[('E', 'English'), ('T', 'Translate'), ('C', 'Create'), ('V', 'Vote')], max_length=1, validators=[django.core.validators.MinLengthValidator(1), django.core.validators.MaxLengthValidator(1)], verbose_name='Kind')),
                ('effort_in_seconds', models.IntegerField(blank=True, null=True, verbose_name='Effort in seconds')),
                ('base', models.CharField(choices=[('k', 'klearing'), ('m', 'modding'), ('a', 'accepting'), ('c', 'creating'), ('t', 'topping'), ('p', 'picking another')], max_length=1, validators=[django.core.validators.MinLengthValidator(1), django.core.validators.MaxLengthValidator(1)], verbose_name='Base')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('assignment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contributions', to='todproof.assignment')),
            ],
        ),
        migrations.CreateModel(
            name='Edit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(blank=True, max_length=1024, null=True, validators=[django.core.validators.MinLengthValidator(0), django.core.validators.MaxLengthValidator(1024)], verbose_name='Content')),
                ('hid', models.BooleanField(default=False, verbose_name='Hidden')),
                ('top', models.CharField(choices=[('N', 'Not top edit'), ('Z', 'Zero vote top edit'), ('T', 'Tie top edit'), ('M', 'Majority top edit')], default='Z', max_length=1, validators=[django.core.validators.MinLengthValidator(1), django.core.validators.MaxLengthValidator(1)], verbose_name='Top Edit')),
                ('mods', models.IntegerField(blank=True, null=True, verbose_name='Mods')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('sentence', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='changes', to='todproof.sentence')),
            ],
        ),
        migrations.RemoveField(
            model_name='change',
            name='sentence',
        ),
        migrations.DeleteModel(
            name='Addition',
        ),
        migrations.DeleteModel(
            name='Change',
        ),
        migrations.AddField(
            model_name='contribution',
            name='base_edit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='todproof.edit'),
        ),
        migrations.AddField(
            model_name='contribution',
            name='edit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contributions', to='todproof.edit'),
        ),
    ]
