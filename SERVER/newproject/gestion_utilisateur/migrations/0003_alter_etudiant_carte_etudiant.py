# Generated by Django 4.2.16 on 2024-10-16 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_utilisateur', '0002_alter_etudiant_carte_etudiant'),
    ]

    operations = [
        migrations.AlterField(
            model_name='etudiant',
            name='carte_etudiant',
            field=models.ImageField(blank=True, null=True, upload_to='qrcodes/'),
        ),
    ]
