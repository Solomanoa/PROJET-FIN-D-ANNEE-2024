# Generated by Django 4.2.16 on 2024-11-04 06:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_utilisateur', '0004_etudiant_niveau'),
        ('enseigner', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='enseigner',
            name='etudiants',
        ),
        migrations.AddField(
            model_name='enseigner',
            name='niveau',
            field=models.CharField(choices=[('L1', 'L1'), ('L2', 'L2'), ('L3', 'L3'), ('M1', 'M1'), ('M2', 'M2')], default='L1', max_length=2),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='enseigner',
            name='enseignant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='enseignements', to='gestion_utilisateur.enseignant'),
        ),
    ]
