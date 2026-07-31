# Django Regon API

REGON/GUS lookup Django module for Volkanos — a thin layer between other Django apps and Polish
government registries: REGON/BIR (`api.stat.gov.pl`, SOAP via `zeep`) and the VAT taxpayers
registry (`wl-api.mf.gov.pl` via `entirius-py-gov-rejestr-wl-sdk`).

## Install

```bash
uv pip install entirius-django-regon-api
```

Add `django_regon_api` to `INSTALLED_APPS`.
Endpoints mount under `{API_BASE_URL}/regon/<version>/` (`nip/<nip>/`, `regon/<regon>/`).

Settings (all optional, sandbox defaults): `BIR_API_KEY`, `BIR_SERVICE_URL`, `BIR_WSDL_URL`,
`BIR_VERSIONS`, `GOV_REJESTR_WL_USE_PROD_ENVIRONMENT`, cache prefixes/timeouts —
reference in [AGENTS.md](AGENTS.md), BIR details in [docs/](docs/README.md).

## Development and testing

```bash
make install   # uv sync, incl. extras
make check     # ruff lint + format-check
make test      # pytest
```
