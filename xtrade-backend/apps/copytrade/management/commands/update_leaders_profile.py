""" Management command to regularly update copy leaders profile."""

import logging

from django.core.management.base import BaseCommand

from copytrade.models import LeadTrader
from exchanges.binance.copytrade import get_leader_profile

logger = logging.getLogger("copytrade")


class Command(BaseCommand):
    """Management command."""

    help = "Updates leader profiles"

    def add_arguments(self, parser):
        parser.add_argument(
            "id",
            type=int,
            nargs="?",
            help="xTrade ID of the trade leader to update profile.",
        )
        parser.add_argument(
            "--dry-run",
            dest="dry_run",
            action="store_const",
            const=True,
            default=False,
            help="Print the output to stdout instead of updating the Leader.",
        )

    def handle(self, *args, **options):
        _id = options["id"]
        dry_run = options["dry_run"]
        if _id:
            try:
                leader = LeadTrader.objects.get(pk=_id)
                leader_profile = get_leader_profile(leader, dry_run=dry_run)
                if dry_run:
                    print(f"{leader_profile=}")
                else:
                    leader.update_profile(leader_profile)
            except LeadTrader.DoesNotExist:
                print(f"Leader with ID {options['id']} does not exist")
        else:
            for leader in LeadTrader.objects.filter(  # pylint: disable=no-member
                check_for_updates=True
            ).select_related("exchange"):
                leader_profile = get_leader_profile(leader, dry_run=dry_run)
                if dry_run:
                    print(f"{leader_profile=}")
                else:
                    leader.update_profile(leader_profile)
