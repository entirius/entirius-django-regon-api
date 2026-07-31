# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.conf import settings

BASE_URL = getattr(settings, "API_BASE_URL", "api").strip("/")

# GUS GOV settings (wl-api.mf.gov.pl - VAT payers only)
GOV_REJESTR_WL_USE_PROD_ENVIRONMENT = getattr(settings, "GOV_REJESTR_WL_USE_PROD_ENVIRONMENT", False)

# REGON API settings (api.stat.gov.pl - all NIPs including personal)
BIR_API_KEY = getattr(settings, "BIR_API_KEY", "abcde12345abcde12345")  # Default test key
BIR_SERVICE_URL = getattr(
    settings, "BIR_SERVICE_URL", "https://wyszukiwarkaregontest.stat.gov.pl/wsBIR/UslugaBIRzewnPubl.svc"
)
BIR_WSDL_URL = getattr(
    settings, "BIR_WSDL_URL", "https://wyszukiwarkaregontest.stat.gov.pl/wsBIR/wsdl/UslugaBIRzewnPubl-ver11-test.wsdl"
)
BIR_VERSIONS = getattr(settings, "BIR_VERSIONS", "bir1.1")

# Cache settings
GET_REGON_DATA_CACHE_PREFIX = getattr(settings, "GET_REGON_DATA_CACHE_PREFIX", "django_regon_api_get_data")
GET_REGON_DATA_CACHE_TIMEOUT = getattr(settings, "GET_REGON_DATA_CACHE_TIMEOUT", 60 * 60 * 1)
GET_GOV_DATA_CACHE_TIMEOUT = getattr(settings, "GET_GOV_DATA_CACHE_TIMEOUT", 60 * 60 * 1)
