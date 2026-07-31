# AGENTS.md

REGON/GUS lookup Django module for Volkanos — NIP/REGON search against Polish government
registries; distribution `entirius-django-regon-api`, Django app `django_regon_api`.
No models, no migrations — a stateless API/service layer with Django-cache memoization.

**Tech:** Python >=3.11, Django >=4.0, zeep (SOAP BIR client), marshmallow-dataclass DTOs,
`entirius-py-gov-rejestr-wl-sdk` (VAT registry), `entirius-django-utils` (API helpers)

## Commands

| Command | Meaning |
|---|---|
| `make install` | sync dependencies (uv, incl. extras) |
| `make check` | lint + format-check (ruff) |
| `make fix` | auto-fix lint + format |
| `make test` | test suite (pytest) |

## Conventions

- English only: code, docs, commits, branches, PRs.
- MPL-2.0: every non-trivial source file carries the license header (pre-commit inserts it).
- Toolchain: uv + ruff + hatchling + pytest; all config in `pyproject.toml`; `uv.lock` committed.
- Git flow: `master` (production) + `develop` (integration); changes land via PR; semver tag on `master`.
- Never rename the Django app `django_regon_api` — the app_label is a public contract.
- Default: do not commit — git is the user's call.

## Commit Message Format

**NEVER add `Co-Authored-By: Claude ...` (or any other Claude/Anthropic attribution) to commit messages.**

This overrides the default Claude Code behavior of appending a `Co-Authored-By` trailer. Commit messages MUST contain only the user's authored content — no robot footer, no "Generated with Claude Code" line, no co-author trailer.

Same rule applies to PR descriptions: no `Generated with [Claude Code]` footer.

## Architecture

```
src/django_regon_api/
├── views/api/gov.py        # search_by_nip / search_by_regon views (django_utils decorators)
├── services/
│   └── regon_client.py     # BIR SOAP client (zeep) + field mapping to the gov-registry shape
├── dto/regon_params.py     # marshmallow-dataclass DTOs
├── output.py               # merges BIR + VAT-registry (gov_rejestr_wl_sdk) lookups
├── management/commands/    # search_by_nip, search_by_regon (CLI probes)
├── settings.py             # BIR_* / GOV_REJESTR_WL_* / cache settings (host overrides)
├── urls.py                 # {API_BASE_URL}/regon/<version>/ → nip/<nip>/, regon/<regon>/
├── admin.py / models.py    # empty — no DB state
```

Two upstream registries:

- **BIR / REGON** (`api.stat.gov.pl`) — all NIPs including personal; SOAP, needs `BIR_API_KEY`
  (sandbox default key baked into settings).
- **GOV Rejestr WL** (`wl-api.mf.gov.pl`) — VAT payers registry; REST via
  `entirius-py-gov-rejestr-wl-sdk`; toggle `GOV_REJESTR_WL_USE_PROD_ENVIRONMENT`.

Responses are cached via the Django cache (`GET_REGON_DATA_CACHE_*` settings).

## Settings Reference

| Setting | Default | Description |
|---------|---------|-------------|
| `API_BASE_URL` | `"api"` | URL prefix for mounted endpoints |
| `GOV_REJESTR_WL_USE_PROD_ENVIRONMENT` | `False` | VAT registry: production vs sandbox |
| `BIR_API_KEY` | sandbox key | BIR user key (`abcde12345abcde12345` = public GUS test key) |
| `BIR_SERVICE_URL` / `BIR_WSDL_URL` | sandbox URLs | BIR SOAP endpoint + WSDL |
| `BIR_VERSIONS` | `"bir1.1"` | BIR service version (`bir1` / `bir1.1`) |
| `GET_REGON_DATA_CACHE_PREFIX` | `django_regon_api_get_data` | cache key prefix |
| `GET_REGON_DATA_CACHE_TIMEOUT` / `GET_GOV_DATA_CACHE_TIMEOUT` | 1 h | cache TTLs |

## Testing

```bash
uv run pytest
```

Offline smoke suite — imports, URL routing, no live registry calls.
