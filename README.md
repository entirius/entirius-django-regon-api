# entirius-django-regon-api

A Django module for Polish company lookups in Entirius, the open-source modular ecommerce platform. Its REST
endpoints search the VAT taxpayers registry by NIP or REGON number, and a Python client looks up any NIP in the
REGON database (BIR).

[![PyPI](https://img.shields.io/pypi/v/entirius-django-regon-api.svg)](https://pypi.org/project/entirius-django-regon-api/)
[![Python](https://img.shields.io/pypi/pyversions/entirius-django-regon-api.svg)](https://pypi.org/project/entirius-django-regon-api/)
[![License: MPL-2.0](https://img.shields.io/badge/license-MPL--2.0-blue.svg)](https://github.com/entirius/entirius-django-regon-api/blob/develop/LICENSE)

## What it does

- Looks up a company by NIP or REGON number over REST endpoints, in the VAT taxpayers registry
  (`wl-api.mf.gov.pl`, through `entirius-py-gov-rejestr-wl-sdk`).
- Looks up a NIP in the REGON database (BIR, `api.stat.gov.pl`) over SOAP from Python code; BIR covers every NIP,
  sole traders included.
- Caches the answers of the Python lookups in the Django cache; keeps no database state (no models, no migrations).
- Ships the `search_by_nip` and `search_by_regon` management commands for probing the VAT registry from the shell.

## Installation

```shell
uv add entirius-django-regon-api
pip install entirius-django-regon-api
```

```python
INSTALLED_APPS = [
    ...
    "django_utils",
    "django_regon_api",
]

# urls.py
urlpatterns = [
    path("", include("django_regon_api.urls")),
]
```

Endpoints mount under `{API_BASE_URL}/regon/<version>/` (`nip/<nip>/`, `regon/<regon>/`).

Every setting is optional and defaults to the registries' public test environments: `BIR_API_KEY`,
`BIR_SERVICE_URL`, `BIR_WSDL_URL`, `BIR_VERSIONS`, `GOV_REJESTR_WL_USE_PROD_ENVIRONMENT`, cache prefix and timeouts;
reference with defaults in https://github.com/entirius/entirius-django-regon-api/blob/develop/AGENTS.md (section
Settings).

## Quick start

```python
from django_regon_api.services.regon_client import RegonApiClient

company = RegonApiClient().search_by_nip("0000000000")
```

`search_by_nip` returns a dictionary in the shape of the VAT registry answer, or `None` when nothing is found.

## Requirements

- Python 3.11 or newer, Django 4.0 or newer.
- Entirius packages pulled in: `entirius-django-utils`, `entirius-py-gov-rejestr-wl-sdk`, `entirius-py-bievents`,
  `entirius-py-process-logger`.

## Documentation

- Module docs: https://github.com/entirius/entirius-django-regon-api/tree/develop/docs
- Entirius documentation: https://docs.entirius.com/
- Releases: https://github.com/entirius/entirius-django-regon-api/releases

## Part of Entirius

This module runs inside the Entirius backend service (Volkanos), where company data is filled in from a tax number.

- Backend service: https://github.com/entirius/entirius-service-volkanos
- Docker harness: https://github.com/entirius/entirius-zeno
- Sibling modules: https://github.com/entirius/entirius-django-utils,
  https://github.com/entirius/entirius-django-accounts
- VAT registry SDK: https://github.com/entirius/entirius-py-gov-rejestr-wl-sdk

## Development

```shell
make install     # sync dependencies (uv)
make check       # lint + format check (ruff)
make test        # test suite (pytest + pytest-django, offline)
```

Development and agent instructions: https://github.com/entirius/entirius-django-regon-api/blob/develop/AGENTS.md

## License

Mozilla Public License 2.0 (MPL-2.0) — see https://github.com/entirius/entirius-django-regon-api/blob/develop/LICENSE.
