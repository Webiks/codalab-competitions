# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-05-19 05:02
from __future__ import unicode_literals

import apps.web.models
import apps.web.storage
from django.conf import settings
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0003_auto_20180404_1817'),
    ]

    operations = [
        migrations.AddField(
            model_name='competitionphase',
            name='ingestion_program_only_during_scoring',
            field=models.BooleanField(default=False, help_text=b'Run ingestion program during scoring, instead of during prediction?'),
        ),
        migrations.AlterField(
            model_name='competition',
            name='admins',
            field=models.ManyToManyField(blank=True, related_name='competition_admins', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='competition',
            name='image',
            field=models.FileField(blank=True, null=True, storage=apps.web.storage.CodalabGoogleCloudStorage(bucket_name=b'coda-public'), upload_to=apps.web.models._uuidify(b'logos'), verbose_name=b'Logo'),
        ),
        migrations.AlterField(
            model_name='competition',
            name='secret_key',
            field=models.UUIDField(default=uuid.UUID('b75012c7-cb30-4f63-8504-56c7f8bbb09c')),
        ),
        migrations.AlterField(
            model_name='competition',
            name='teams',
            field=models.ManyToManyField(blank=True, related_name='competition_teams', to='teams.Team'),
        ),
        migrations.AlterField(
            model_name='competitiondefbundle',
            name='config_bundle',
            field=models.FileField(blank=True, null=True, storage=apps.web.storage.CodalabGoogleCloudStorage(bucket_name=b'coda-private'), upload_to=apps.web.models._uuidify(b'competition-bundles')),
        ),
        migrations.AlterField(
            model_name='competitiondump',
            name='data_file',
            field=models.FileField(blank=True, null=True, storage=apps.web.storage.CodalabGoogleCloudStorage(bucket_name=b'coda-private'), upload_to=apps.web.models._uuidify(b'competition_dump'), verbose_name=b'Data file'),
        ),
        migrations.AlterField(
            model_name='competitionphase',
            name='ingestion_program',
            field=models.FileField(blank=True, null=True, storage=apps.web.storage.CodalabGoogleCloudStorage(bucket_name=b'coda-private'), upload_to=apps.web.models._uuidify(b'ingestion_program')),
        ),
        migrations.AlterField(
            model_name='competitionphase',
            name='input_data',
            field=models.FileField(blank=True, null=True, storage=apps.web.storage.CodalabGoogleCloudStorage(bucket_name=b'coda-private'), upload_to=apps.web.models._uuidify(b'phase_input_data_file'), verbose_name=b'Input Data'),
        ),
        migrations.AlterField(
            model_name='competitionphase',
            name='public_data',
            field=models.FileField(blank=True, null=True, storage=apps.web.storage.CodalabGoogleCloudStorage(bucket_name=b'coda-private'), upload_to=apps.web.models._uuidify(b'public_data'), verbose_name=b'Public Data'),
        ),
        migrations.AlterField(
            model_name='competitionphase',
            name='reference_data',
            field=models.FileField(blank=True, null=True, storage=apps.web.storage.CodalabGoogleCloudStorage(bucket_name=b'coda-private'), upload_to=apps.web.models._uuidify(b'phase_reference_data_file'), verbose_name=b'Reference Data'),
        ),
        migrations.AlterField(
            model_name='competitionphase',
            name='scoring_program',
            field=models.FileField(blank=True, null=True, storage=apps.web.storage.CodalabGoogleCloudStorage(bucket_name=b'coda-private'), upload_to=apps.web.models._uuidify(b'phase_scoring_program_file'), verbose_name=b'Scoring Program'),
        ),
        migrations.AlterField(
            model_name='competitionphase',
            name='starting_kit',
            field=models.FileField(blank=True, null=True, storage=apps.web.storage.CodalabGoogleCloudStorage(bucket_name=b'coda-private'), upload_to=apps.web.models._uuidify(b'starting_kit'), verbose_name=b'Starting Kit'),
        ),
        migrations.AlterField(
            model_name='competitionsubmission',
            name='coopetition_file',
            field=models.FileField(blank=True, null=True, storage=apps.web.storage.CodalabGoogleCloudStorage(bucket_name=b'coda-private'), upload_to=apps.web.models._uuidify(b'submission_coopetition')),
        ),
        migrations.AlterField(
            model_name='competitionsubmission',
            name='detailed_results_file',
            field=models.FileField(blank=True, null=True, storage=apps.web.storage.CodalabGoogleCloudStorage(bucket_name=b'coda-private'), upload_to=apps.web.models._uuidify(b'submission_detailed_results')),
        ),
        migrations.AlterField(
            model_name='competitionsubmission',
            name='file',
            field=models.FileField(blank=True, null=True, storage=apps.web.storage.CodalabGoogleCloudStorage(bucket_name=b'coda-private'), upload_to=b''),
        ),
        migrations.AlterField(
            model_name='competitionsubmission',
            name='history_file',
            field=models.FileField(blank=True, null=True, storage=apps.web.storage.CodalabGoogleCloudStorage(bucket_name=b'coda-private'), upload_to=apps.web.models._uuidify(b'submission_history')),
        ),
        migrations.AlterField(
            model_name='competitionsubmission',
            name='ingestion_program_stderr_file',
            field=models.FileField(blank=True, null=True, storage=apps.web.storage.CodalabGoogleCloudStorage(bucket_name=b'coda-private'), upload_to=apps.web.models._uuidify(b'predict_submission_stderr')),
        ),
        migrations.AlterField(
            model_name='competitionsubmission',
            name='ingestion_program_stdout_file',
            field=models.FileField(blank=True, null=True, storage=apps.web.storage.CodalabGoogleCloudStorage(bucket_name=b'coda-private'), upload_to=apps.web.models._uuidify(b'predict_submission_stdout')),
        ),
        migrations.AlterField(
            model_name='competitionsubmission',
            name='inputfile',
            field=models.FileField(blank=True, null=True, storage=apps.web.storage.CodalabGoogleCloudStorage(bucket_name=b'coda-private'), upload_to=apps.web.models._uuidify(b'submission_inputfile')),
        ),
        migrations.AlterField(
            model_name='competitionsubmission',
            name='output_file',
            field=models.FileField(blank=True, null=True, storage=apps.web.storage.CodalabGoogleCloudStorage(bucket_name=b'coda-private'), upload_to=apps.web.models._uuidify(b'submission_output')),
        ),
        migrations.AlterField(
            model_name='competitionsubmission',
            name='prediction_output_file',
            field=models.FileField(blank=True, null=True, storage=apps.web.storage.CodalabGoogleCloudStorage(bucket_name=b'coda-private'), upload_to=apps.web.models._uuidify(b'submission_prediction_output')),
        ),
        migrations.AlterField(
            model_name='competitionsubmission',
            name='prediction_runfile',
            field=models.FileField(blank=True, null=True, storage=apps.web.storage.CodalabGoogleCloudStorage(bucket_name=b'coda-private'), upload_to=apps.web.models._uuidify(b'submission_prediction_runfile')),
        ),
        migrations.AlterField(
            model_name='competitionsubmission',
            name='prediction_stderr_file',
            field=models.FileField(blank=True, null=True, storage=apps.web.storage.CodalabGoogleCloudStorage(bucket_name=b'coda-private'), upload_to=apps.web.models._uuidify(b'predict_submission_stderr')),
        ),
        migrations.AlterField(
            model_name='competitionsubmission',
            name='prediction_stdout_file',
            field=models.FileField(blank=True, null=True, storage=apps.web.storage.CodalabGoogleCloudStorage(bucket_name=b'coda-private'), upload_to=apps.web.models._uuidify(b'predict_submission_stdout')),
        ),
        migrations.AlterField(
            model_name='competitionsubmission',
            name='private_output_file',
            field=models.FileField(blank=True, null=True, storage=apps.web.storage.CodalabGoogleCloudStorage(bucket_name=b'coda-private'), upload_to=apps.web.models._uuidify(b'submission_private_output')),
        ),
        migrations.AlterField(
            model_name='competitionsubmission',
            name='runfile',
            field=models.FileField(blank=True, null=True, storage=apps.web.storage.CodalabGoogleCloudStorage(bucket_name=b'coda-private'), upload_to=apps.web.models._uuidify(b'submission_runfile')),
        ),
        migrations.AlterField(
            model_name='competitionsubmission',
            name='scores_file',
            field=models.FileField(blank=True, null=True, storage=apps.web.storage.CodalabGoogleCloudStorage(bucket_name=b'coda-private'), upload_to=apps.web.models._uuidify(b'submission_scores')),
        ),
        migrations.AlterField(
            model_name='competitionsubmission',
            name='stderr_file',
            field=models.FileField(blank=True, null=True, storage=apps.web.storage.CodalabGoogleCloudStorage(bucket_name=b'coda-private'), upload_to=apps.web.models._uuidify(b'submission_stderr')),
        ),
        migrations.AlterField(
            model_name='competitionsubmission',
            name='stdout_file',
            field=models.FileField(blank=True, null=True, storage=apps.web.storage.CodalabGoogleCloudStorage(bucket_name=b'coda-private'), upload_to=apps.web.models._uuidify(b'submission_stdout')),
        ),
        migrations.AlterField(
            model_name='organizerdataset',
            name='data_file',
            field=models.FileField(blank=True, null=True, storage=apps.web.storage.CodalabGoogleCloudStorage(bucket_name=b'coda-private'), upload_to=apps.web.models._uuidify(b'dataset_data_file'), verbose_name=b'Data file'),
        ),
        migrations.AlterField(
            model_name='organizerdataset',
            name='sub_data_files',
            field=models.ManyToManyField(blank=True, to='web.OrganizerDataSet', verbose_name=b'Bundle of data files'),
        ),
    ]