# Generated by Django 2.0.6 on 2018-06-08 19:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0006_vote_last_updated'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='vote',
            options={'ordering': ['-created']},
        ),
        migrations.RenameField(
            model_name='vote',
            old_name='last_updated',
            new_name='created',
        ),
        migrations.RemoveField(
            model_name='choice',
            name='votes',
        ),
        migrations.RemoveField(
            model_name='vote',
            name='num',
        ),
        migrations.AlterField(
            model_name='choice',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='choices', to='polls.Question'),
        ),
        migrations.AlterField(
            model_name='vote',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
