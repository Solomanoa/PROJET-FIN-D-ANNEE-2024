# Generated by Django 4.2.16 on 2024-11-03 20:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_utilisateur', '0004_etudiant_niveau'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='enseignant',
            name='id',
        ),
        migrations.RemoveField(
            model_name='etudiant',
            name='id',
        ),
        migrations.RemoveField(
            model_name='responsablepedagogique',
            name='id',
        ),
        migrations.AlterField(
            model_name='enseignant',
            name='utilisateur',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='gestion_utilisateur.utilisateur'),
        ),
        migrations.AlterField(
            model_name='etudiant',
            name='utilisateur',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='gestion_utilisateur.utilisateur'),
        ),
        migrations.AlterField(
            model_name='responsablepedagogique',
            name='utilisateur',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='gestion_utilisateur.utilisateur'),
        ),
    ]