# Generated by Django 3.1.4 on 2021-03-02 04:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_remove_comments_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='comments',
            name='user',
            field=models.CharField(default='yuvio100', max_length=64),
            preserve_default=False,
        ),
    ]
