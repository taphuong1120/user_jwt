from datetime import datetime
from django.db import migrations


def add_user(apps, schema_editor):
    users = [
        {
            'id': 1, 
            'username': 'taphuong', 
            'email': 'taphuong@gmail.com',
            'password': 'phuong2000',
        },

        {
            'id': 2, 
            'username': 'phuongta', 
            'email': 'phuongta@gmail.com',
            'password': 'phuong2000',
        }
    ]
    User = apps.get_model('user', 'Users')

    for user in users:
        currentModel = User(
            id=user['id'],
            username=user['username'],
            email=user['email'],
            # twitter=user['twitter'],
            # telegram=user['telegram'],
            # bio=user['bio'],
            # wallet=user['wallet'],
            # dnft=user['dnft'],
            # dp=user['user'],
            password=user['password'],
            # photo=user['photo'],
            # role=user['role'],
            # disabled=user['disabled'],
            created_at=datetime.now(),
        )
        currentModel.save()


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_user),
    ]
