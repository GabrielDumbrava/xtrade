"""Signals related to copy trading."""

import logging
import django.dispatch
from django.dispatch import receiver

copytrade_seats_available_signal = django.dispatch.Signal()

logger = logging.getLogger("copytrade")


@receiver(copytrade_seats_available_signal, dispatch_uid="copytrade_seats_available")
def copytrade_seats_available(sender, **kwargs):  # pylint: disable=unused-argument
    """This signal will be triggered when a lead trader has new seats available."""
    logger.info(
        "Seats available for leader %s, %s", kwargs["leader_name"], kwargs["leader_url"]
    )
