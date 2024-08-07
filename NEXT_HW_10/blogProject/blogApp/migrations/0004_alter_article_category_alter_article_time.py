# Generated by Django 5.0.4 on 2024-04-06 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogApp', '0003_article_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='category',
            field=models.TextField(choices=[('option1', '취미'), ('option2', '음식'), ('option3', '프로그래밍')], default='option1'),
        ),
        migrations.AlterField(
            model_name='article',
            name='time',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
