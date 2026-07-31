# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

# Offline smoke suite — imports, URL routing, DTO round-trip. No live registry calls.

from importlib import import_module

import pytest
from django.urls import resolve, reverse

MODULES = [
    "django_regon_api",
    "django_regon_api.admin",
    "django_regon_api.apps",
    "django_regon_api.dto.regon_params",
    "django_regon_api.management.commands.search_by_nip",
    "django_regon_api.management.commands.search_by_regon",
    "django_regon_api.output",
    "django_regon_api.services.regon_client",
    "django_regon_api.settings",
    "django_regon_api.urls",
    "django_regon_api.views.api.gov",
]


@pytest.mark.parametrize("module", MODULES)
def test_module_imports(module):
    import_module(module)


def test_nip_route_resolves():
    url = reverse("gov-rejestr-wl-nip", kwargs={"version": "v1", "nip": "0000000000"})
    assert url == "/api/regon/v1/nip/0000000000/"
    assert resolve(url).view_name == "gov-rejestr-wl-nip"


def test_regon_route_resolves():
    url = reverse("gov-rejestr-wl-regon", kwargs={"version": "v1", "regon": "000000000"})
    assert url == "/api/regon/v1/regon/000000000/"
    assert resolve(url).view_name == "gov-rejestr-wl-regon"
