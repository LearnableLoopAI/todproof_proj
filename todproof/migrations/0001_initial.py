# Generated by Django 3.2.5 on 2021-08-05 15:35

import datetime
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dod', models.DateField(verbose_name='Date Of Delivery')),
                ('tod', models.CharField(choices=[('n', 'No Time Of Day'), ('s', 'Sunrise'), ('b', 'Breakfast'), ('x', 'Morning'), ('y', 'Afternoon'), ('z', 'Evening')], default='n', max_length=1, validators=[django.core.validators.MinLengthValidator(1), django.core.validators.MaxLengthValidator(1)], verbose_name='Time Of Day')),
                ('dow', models.CharField(choices=[('su', 'Sunday'), ('mo', 'Monday'), ('tu', 'Tuesday'), ('we', 'Wednesday'), ('th', 'Thursday'), ('fr', 'Friday'), ('sa', 'Saturday')], default='su', max_length=2, verbose_name='Day Of Week')),
                ('title', models.CharField(max_length=64, verbose_name='Document Title')),
                ('descriptor', models.CharField(max_length=120, verbose_name='Descriptor')),
            ],
        ),
        migrations.CreateModel(
            name='Translation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lan', models.CharField(max_length=3, verbose_name='Language')),
                ('tran_title', models.CharField(max_length=70, verbose_name='Translated title')),
                ('descrip', models.TextField(blank=True, max_length=500, null=True, verbose_name='Description')),
                ('blkc', models.IntegerField(verbose_name='Block count')),
                ('subc', models.IntegerField(verbose_name='Sub-block count')),
                ('senc', models.IntegerField(verbose_name='Sentence count')),
                ('xcrip', models.CharField(choices=[('A', 'Andes'), ('M', 'Mamalis')], default='A', max_length=1, verbose_name='Transcription')),
                ('li', models.BooleanField(verbose_name='Lookup imported (eng) / translate contributions randomized (oth)')),
                ('pubdate', models.DateField(default=datetime.date.today, verbose_name='Publication date')),
                ('version', models.CharField(max_length=20, verbose_name='Version')),
                ('document', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='todproof.document')),
                ('eng_tran', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='todproof.translation')),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('EP', 'English Provider (EP)'), ('EE', 'English Editor (EE)'), ('NT', 'No Translator (NT)'), ('MT', 'Machine Translator (MT)'), ('HT', 'Human Translator (HT)'), ('TE', 'Translation Editor (TE)'), ('SE', 'Scripture Editor (SE)'), ('PE', 'Poetry Editor (PE)'), ('CE', 'Chief Editor (CE)'), ('LA', 'Language Administrator (LA)')], default='TE', max_length=2, validators=[django.core.validators.MinLengthValidator(2), django.core.validators.MaxLengthValidator(2)], verbose_name='Role')),
                ('active', models.BooleanField(default=False, verbose_name='Active')),
                ('place', models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)], verbose_name='Place')),
                ('ci', models.BooleanField(default=False, verbose_name='Content imported')),
                ('status', models.CharField(choices=[('ip', 'In Process (ip)'), ('cd', 'Completed (cd)'), ('te', 'TE editing (te)'), ('ce', 'CE editing (ce)'), ('qe', 'QE editing (qe)'), ('pg', 'Publishing (pg)'), ('pd', 'Published (pd)'), ('pr', 'Pruned (pr)')], default='ip', max_length=2, validators=[django.core.validators.MinLengthValidator(2), django.core.validators.MaxLengthValidator(2)], verbose_name='Status')),
                ('ccs', models.IntegerField(blank=True, null=True, verbose_name='Final Create additions')),
                ('ccs_k', models.IntegerField(blank=True, null=True, verbose_name='- by klearing')),
                ('ccs_m', models.IntegerField(blank=True, null=True, verbose_name='- by modding')),
                ('vcs', models.IntegerField(blank=True, null=True, verbose_name='Final Vote additions')),
                ('vcs_a', models.IntegerField(blank=True, null=True, verbose_name='- by accepting')),
                ('vcs_c', models.IntegerField(blank=True, null=True, verbose_name='- by creating')),
                ('vcs_t', models.IntegerField(blank=True, null=True, verbose_name='- by topping')),
                ('vcs_p', models.IntegerField(blank=True, null=True, verbose_name='- by picking')),
                ('ct', models.IntegerField(blank=True, null=True, verbose_name='Final Create time (s)')),
                ('vt', models.IntegerField(blank=True, null=True, verbose_name='Final Vote time (s)')),
                ('majtes', models.IntegerField(blank=True, null=True, verbose_name='Final Majority Top Changes')),
                ('tietes', models.IntegerField(blank=True, null=True, verbose_name='Final Tie Top Changes')),
                ('notes', models.CharField(blank=True, max_length=200, null=True, verbose_name='Notes')),
                ('translation', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='tasks', to='todproof.translation')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='tasks', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Sentence',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('blk', models.IntegerField(blank=True, null=True, verbose_name='Block')),
                ('sub', models.IntegerField(blank=True, null=True, verbose_name='Sub-block')),
                ('rsub', models.IntegerField(blank=True, null=True, verbose_name='Running sub-block')),
                ('sen', models.IntegerField(blank=True, null=True, verbose_name='Sentence')),
                ('rsen', models.IntegerField(blank=True, null=True, verbose_name='Running sentence')),
                ('typ', models.CharField(choices=[('n', 'Normal'), ('c', 'Conversation'), ('s', 'Scripture'), ('p', 'Poetry first line'), ('q', 'Poetry other lines')], default='n', max_length=1, validators=[django.core.validators.MinLengthValidator(1), django.core.validators.MaxLengthValidator(1)], verbose_name='Sentence type')),
                ('tie', models.BooleanField(default=False, verbose_name='Tie')),
                ('translation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sentences', to='todproof.translation')),
            ],
        ),
        migrations.CreateModel(
            name='Lookup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('blk', models.IntegerField(blank=True, null=True, verbose_name='Block')),
                ('rsub', models.IntegerField(blank=True, null=True, verbose_name='Running sub-block')),
                ('sub', models.IntegerField(blank=True, null=True, verbose_name='Sub-block')),
                ('translation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lookups', to='todproof.translation')),
            ],
        ),
        migrations.CreateModel(
            name='Change',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(blank=True, max_length=1024, null=True, validators=[django.core.validators.MinLengthValidator(0), django.core.validators.MaxLengthValidator(1024)], verbose_name='Content')),
                ('hid', models.BooleanField(default=False, verbose_name='Hidden')),
                ('top', models.CharField(choices=[('N', 'Not top change'), ('Z', 'Zero vote top change'), ('T', 'Tie top change'), ('M', 'Majority top change')], default='Z', max_length=1, validators=[django.core.validators.MinLengthValidator(1), django.core.validators.MaxLengthValidator(1)], verbose_name='Top Change')),
                ('mods', models.IntegerField(blank=True, null=True, verbose_name='Mods')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('sentence', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='changes', to='todproof.sentence')),
            ],
        ),
        migrations.CreateModel(
            name='Addition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kind', models.CharField(choices=[('E', 'English'), ('T', 'Translate'), ('C', 'Create'), ('V', 'Vote')], max_length=1, validators=[django.core.validators.MinLengthValidator(1), django.core.validators.MaxLengthValidator(1)], verbose_name='Kind')),
                ('effort_in_seconds', models.IntegerField(blank=True, null=True, verbose_name='Effort in seconds')),
                ('base', models.CharField(choices=[('k', 'clearing'), ('m', 'modding'), ('a', 'accepting'), ('c', 'creating'), ('t', 'topping'), ('p', 'picking another')], max_length=1, validators=[django.core.validators.MinLengthValidator(1), django.core.validators.MaxLengthValidator(1)], verbose_name='Base')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('base_change', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='todproof.change')),
                ('change', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='additions', to='todproof.change')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='additions', to='todproof.task')),
            ],
        ),
    ]
