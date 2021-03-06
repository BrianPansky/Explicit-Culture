# Generated by Django 2.1 on 2018-10-23 03:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='appliedEval',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('evaluation', models.DecimalField(decimal_places=2, max_digits=2)),
            ],
        ),
        migrations.CreateModel(
            name='evalType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True)),
                ('description', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='identity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('b', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='identifierPeople', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ontology',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True)),
                ('description', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='referentStandIn',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True)),
                ('description', models.CharField(max_length=100)),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='ontologies', to='evalapp.ontology')),
            ],
        ),
        migrations.AddField(
            model_name='identity',
            name='referentStandInIfAny',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='referentStandInsIfAny', to='evalapp.referentStandIn'),
        ),
        migrations.AddField(
            model_name='identity',
            name='userIfAny',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='usersIfAny', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='appliedeval',
            name='appliedTo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='referentStandInEvalApplyees', to='evalapp.identity'),
        ),
        migrations.AddField(
            model_name='appliedeval',
            name='typeApplied',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='appliedEvals', to='evalapp.evalType'),
        ),
    ]
