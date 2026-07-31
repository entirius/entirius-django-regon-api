# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.urls import include, path

from . import settings
from .views import api

paths = [
    path("nip/<str:nip>/", api.search_by_nip, name="gov-rejestr-wl-nip"),
    path("regon/<str:regon>/", api.search_by_regon, name="gov-rejestr-wl-regon"),
]

urlpatterns = [path(f"{settings.BASE_URL}/regon/<str:version>/", include(paths))]
