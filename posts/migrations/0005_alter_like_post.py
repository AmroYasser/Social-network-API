# Generated by Django 4.1.5 on 2023-01-21 15:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("posts", "0004_alter_like_post_alter_like_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="like",
            name="post",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="posts.post"
            ),
        ),
    ]
