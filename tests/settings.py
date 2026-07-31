# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

SECRET_KEY = "not-so-secret-test-key"  # noqa: S105
USE_TZ = True
DEBUG = True
ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.auth",
    "django_regional",  # django_utils imports django_regional.models at import time
    "django_regon_api",
]

# No models — sqlite in-memory satisfies the test runner without external services.
DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}}

ROOT_URLCONF = "django_regon_api.urls"
