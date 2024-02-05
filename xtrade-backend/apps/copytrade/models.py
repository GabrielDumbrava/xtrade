""" Models for CopyTrade module. """

from django.db import models

from xtrade.models import Exchange
from copytrade.signals import copytrade_seats_available_signal


class LeadTrader(models.Model):
    """A LeadTrader model."""

    exchange = models.ForeignKey(
        Exchange, on_delete=models.PROTECT, null=True, blank=True
    )
    name = models.CharField(max_length=255)
    original_name = models.CharField(
        max_length=200,
        default="",
        blank=True,
        null=False,
        help_text="Used in case the trader has a localized name (Chinese for example).",
    )
    profile_url = models.URLField("Profile URL", blank=True, null=False, default="")
    status_available = models.BooleanField(
        "Available for copy", help_text="If there are available spots to be copied."
    )
    status_copy = models.BooleanField(
        "I am copying", help_text="If I'm already copying this trader", default=False
    )
    status_mock_copy = models.BooleanField(
        "I am mock copying",
        help_text="If I'm already mock copying this trader",
        default=False,
    )
    notify_on_availability = models.BooleanField(default=False)
    minimum_copy_amount = models.CharField(
        max_length=50, default="", blank=True, null=False
    )
    check_for_updates = models.BooleanField(default=False, blank=False, null=False)
    profile = models.JSONField(null=True, blank=True, default=dict)

    def update_profile(self, profile: dict):
        """Update lead trader profile. Also trigger signal if new slots are available."""
        if not profile:
            return
        if not self.status_available and profile.get("copiers", 0) < profile.get(
            "seats", 0
        ):
            # There are available copy seats
            self.status_available = True
            # Trigger new seats signal
            # TODO: make it async
            if self.notify_on_availability:
                copytrade_seats_available_signal.send(
                    sender=self.__class__,
                    leader_name=self.name,
                    leader_url=self.profile_url,
                )
        _updated_profile = dict(self.profile)
        _updated_profile.update(profile)
        self.profile = _updated_profile
        self.save()

    def __str__(self):
        return str(self.name)
