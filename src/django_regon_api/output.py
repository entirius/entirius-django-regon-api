# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from typing import Any

from django.core.cache import cache
from gov_rejestr_wl_sdk.services.client import GovRejestrWL
from process_logger import ProcessLogger

from django_regon_api import settings
from django_regon_api.settings import GOV_REJESTR_WL_USE_PROD_ENVIRONMENT

logger = ProcessLogger("django_regon_api.output")


def get_cache_key(nip: str, prefix: str = None) -> str:
    return f"{prefix}:{nip}"


# used by
# django_vat_validator
def get_nip_from_gov(nip: str) -> tuple[Any, dict[str, Any] | None]:
    """
    Check if the provided NIP is a valid VAT payer using GUS GOV API (wl-api.mf.gov.pl).

    This API only returns data for active VAT payers.
    Personal NIPs that are not VAT registered will return null.

    :param nip: The NIP to validate.
    :return: Tuple (is_valid, data) - True if NIP is VAT registered, False otherwise.
    """

    if len(nip) > 2 and nip[:2].isalpha():
        nip = nip[2:]
    try:
        cache_key = get_cache_key(nip, "django_regon_api_gus_gov")
        cached_data = cache.get(cache_key)
        if cached_data:
            return True, cached_data

        client = GovRejestrWL(use_prod_environment=GOV_REJESTR_WL_USE_PROD_ENVIRONMENT)
        result = client.search_by_nip(nip, return_transformed=True)

        cache.set(cache_key, result, settings.GET_GOV_DATA_CACHE_TIMEOUT)
        return True, result
    except Exception as e:
        logger.exception(e)
        return False, None


# used by
# django_vat_validator
def get_nip_from_regon_api(nip: str) -> tuple[bool, dict[str, Any] | None]:
    """
    Check if the provided NIP exists in REGON database (api.stat.gov.pl).

    This API returns data for ALL registered entities including:
    - Active VAT payers
    - Personal NIPs (not VAT registered)
    - Inactive entities

    This is the proper way to validate if a NIP exists and get entity data,
    regardless of VAT registration status.

    :param nip: The NIP to validate (without country prefix).
    :return: Tuple (is_valid, data) - True if NIP exists in REGON, False otherwise.
    """
    if len(nip) > 2 and nip[:2].isalpha():
        nip = nip[2:]

    try:
        from django_regon_api.services.regon_client import RegonApiClient

        cache_key = get_cache_key(nip, "django_regon_api_regon")
        cached_data = cache.get(cache_key)
        if cached_data:
            return True, cached_data

        client = RegonApiClient()
        result = client.search_by_nip(nip, return_transformed=True)
        if result:
            cache.set(cache_key, result, settings.GET_REGON_DATA_CACHE_TIMEOUT)
            return True, result
        else:
            return False, None

    except Exception as e:
        logger.exception(e)
        return False, None
