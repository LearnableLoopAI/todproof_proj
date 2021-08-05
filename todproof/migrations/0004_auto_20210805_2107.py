# Generated by Django 3.2.5 on 2021-08-05 21:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('todproof', '0003_auto_20210805_2049'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='translation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='assignments', to='todproof.translation'),
        ),
        migrations.AlterField(
            model_name='assignment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='assignments', to=settings.AUTH_USER_MODEL),
        ),
    ]