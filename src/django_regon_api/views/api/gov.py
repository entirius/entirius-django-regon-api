# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import logging

from django_utils.api.decorators import api_view, parse_parameters, require_http_method
from django_utils.api.exceptions import BadRequest
from django_utils.api.responses import Response
from gov_rejestr_wl_sdk.services.client import GovRejestrWL

from django_regon_api.dto.regon_params import RegonParams
from django_regon_api.settings import GOV_REJESTR_WL_USE_PROD_ENVIRONMENT

logger = logging.getLogger("debug")


@api_view
@parse_parameters(RegonParams.Schema())
@require_http_method("GET")
def search_by_nip(request, params: RegonParams, nip, *args, **kwargs):
    # NIP
    exception_code = 5001
    try:
        client = GovRejestrWL(use_prod_environment=GOV_REJESTR_WL_USE_PROD_ENVIRONMENT)
        result = client.search_by_nip(nip, return_transformed=not params.raw_gus_data)
        return Response(result)
    except Exception as e:
        logger.exception(e, extra={"code": exception_code})
        raise BadRequest("No data found", exception_code) from e


@api_view
@parse_parameters(RegonParams.Schema())
@require_http_method("GET")
def search_by_regon(request, params: RegonParams, regon, *args, **kwargs):
    # REGON
    exception_code = 5003
    try:
        client = GovRejestrWL(use_prod_environment=GOV_REJESTR_WL_USE_PROD_ENVIRONMENT)
        result = client.search_by_regon(regon, return_transformed=not params.raw_gus_data)
        return Response(result)
    except Exception as e:
        logger.exception(e, extra={"code": exception_code})
        raise BadRequest("No data found", exception_code) from e
