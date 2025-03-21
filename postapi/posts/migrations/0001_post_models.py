# Generated by Django 5.1.7 on 2025-03-09 07:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Post",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("description", models.CharField(max_length=1024)),
                ("keywords", models.TextField(max_length=500)),
                ("url", models.URLField(max_length=1024)),
                ("author_ip", models.GenericIPAddressField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="PostHistory",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("original_post_id", models.IntegerField(blank=True, null=True)),
                (
                    "operation",
                    models.CharField(
                        choices=[("update", "Update"), ("delete", "Delete")],
                        max_length=10,
                    ),
                ),
                ("data", models.JSONField()),
                ("modified_at", models.DateTimeField(auto_now_add=True)),
                ("modified_by_ip", models.GenericIPAddressField()),
                (
                    "post",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="histories",
                        to="posts.post",
                    ),
                ),
            ],
        ),
    ]
