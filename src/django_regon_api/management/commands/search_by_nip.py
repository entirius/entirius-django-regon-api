# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from bievents import bi_django_command_decorator
from django.core.management.base import BaseCommand
from gov_rejestr_wl_sdk.services.client import GovRejestrWL


class Command(BaseCommand):
    help = "Import data from gov-rejestr-wl by NIP"

    def add_arguments(self, parser):
        parser.add_argument("nip", type=str)

    @bi_django_command_decorator
    def handle(self, *args, **options):
        nip = options["nip"]
        print(f"NIP: {nip}")
        client = GovRejestrWL()
        result = client.search_by_nip(nip)
        print(result)
