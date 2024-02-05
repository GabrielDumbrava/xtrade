# Generated by Django 5.0.1 on 2024-02-05 12:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("xtrade", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="LeadTrader",
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
                ("name", models.CharField(max_length=255)),
                (
                    "original_name",
                    models.CharField(
                        blank=True,
                        default="",
                        help_text="Used in case the trader has a localized name (Chinese for example).",
                        max_length=200,
                    ),
                ),
                (
                    "profile_url",
                    models.URLField(blank=True, default="", verbose_name="Profile URL"),
                ),
                (
                    "status_available",
                    models.BooleanField(
                        help_text="If there are available spots to be copied.",
                        verbose_name="Available for copy",
                    ),
                ),
                (
                    "status_copy",
                    models.BooleanField(
                        default=False,
                        help_text="If I'm already copying this trader",
                        verbose_name="I am copying",
                    ),
                ),
                (
                    "status_mock_copy",
                    models.BooleanField(
                        default=False,
                        help_text="If I'm already mock copying this trader",
                        verbose_name="I am mock copying",
                    ),
                ),
                ("notify_on_availability", models.BooleanField(default=False)),
                (
                    "minimum_copy_amount",
                    models.CharField(blank=True, default="", max_length=50),
                ),
                ("check_for_updates", models.BooleanField(default=False)),
                ("profile", models.JSONField(blank=True, default=dict, null=True)),
                (
                    "exchange",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="xtrade.exchange",
                    ),
                ),
            ],
        ),
    ]