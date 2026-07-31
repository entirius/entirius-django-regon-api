# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


from bievents import bi_django_command_decorator
from django.core.management.base import BaseCommand
from gov_rejestr_wl_sdk.services.client import GovRejestrWL


class Command(BaseCommand):
    help = "Import data from gov-rejestr-wl by REGON"

    def add_arguments(self, parser):
        parser.add_argument("regon", type=str)

    @bi_django_command_decorator
    def handle(self, *args, **options):
        regon = options["regon"]
        print(f"regon: {regon}")
        client = GovRejestrWL()
        result = client.search_by_regon(regon)
        print(result)
