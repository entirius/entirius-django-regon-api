# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

"""
REGON API Client for BIR1 service (stat.gov.pl)

This client communicates with the official Polish Statistical Office (GUS)
REGON database API (BIR1) which provides data for all registered entities,
including personal taxpayer NIPs that are not VAT registered.

API Documentation: https://api.stat.gov.pl/Home/RegonApi
"""

from typing import Any

from django.core.cache import cache
from process_logger import ProcessLogger, ProcessLoggerMixin
from zeep import Client
from zeep.cache import SqliteCache
from zeep.plugins import HistoryPlugin
from zeep.transports import Transport

from django_regon_api import settings


class RegonApiClient(ProcessLoggerMixin):
    """
    Client for REGON API (BIR1) - validates all NIPs including personal NIPs.

    This is different from GUS_GOV provider which uses wl-api.mf.gov.pl
    and only returns VAT registered entities.
    """

    def __init__(self, api_key: str = None, service_url: str = None, wsdl_url: str = None):
        self._api_key = api_key or settings.BIR_API_KEY
        self._service_url = service_url or settings.BIR_SERVICE_URL
        self._wsdl_url = wsdl_url or settings.BIR_WSDL_URL
        self._session_id = None
        self._client = None
        self._history = HistoryPlugin()
        self.logger = ProcessLogger("django_regon_api.services.RegonApiClient")

    def _get_client(self) -> Client:
        """Get or create SOAP client."""
        if not self._client:
            transport = Transport(cache=SqliteCache())
            self._client = Client(wsdl=self._wsdl_url, transport=transport, plugins=[self._history])
            self._client.service._binding_options["address"] = self._service_url
        return self._client

    def _login(self) -> str:
        """Login to REGON API and get session ID."""
        if self._session_id:
            return self._session_id

        try:
            client = self._get_client()
            self._session_id = client.service.Zaloguj(self._api_key)
            return self._session_id
        except Exception as e:
            self.logger.exception(e)
            raise

    def _logout(self):
        """Logout from REGON API."""
        if self._session_id:
            try:
                client = self._get_client()
                client.service.Wyloguj(self._session_id)
                self._session_id = None
            except Exception as e:
                self.logger.exception(e)

    def _set_session_header(self):
        """Set session ID in SOAP header."""
        self._login()
        self._get_client().transport.session.headers.update({"sid": self._session_id})

    def get_cache_key(self, nip: str) -> str:
        """Generate cache key for NIP."""
        return f"{settings.GET_REGON_DATA_CACHE_PREFIX}:regon:{nip}"

    def search_by_nip(self, nip: str, return_transformed: bool = True) -> dict[str, Any] | None:
        """
        Search entity by NIP in REGON database.

        Args:
            nip: NIP number (without country prefix)
            return_transformed: Whether to return transformed data

        Returns:
            Dictionary with entity data or None if not found
        """
        cache_key = self.get_cache_key(nip)
        cached_data = cache.get(cache_key)
        if cached_data:
            return cached_data
        try:
            self._set_session_header()
            client = self._get_client()
            result = client.service.DaneSzukajPodmioty(pParametryWyszukiwania={"Nip": nip})

            if not result or result == "":
                self.logger.info(f"No entity found for NIP: {nip}")
                return None

            import xml.etree.ElementTree as ET

            root = ET.fromstring(result)  # noqa: S314 — BIR SOAP payload; defusedxml swap tracked as tech debt

            regon = None
            for dane in root.findall(".//dane"):
                regon_elem = dane.find("Regon")
                if regon_elem is not None:
                    regon = regon_elem.text
                    break

            if not regon:
                self.logger.warning(f"REGON not found in response for NIP: {nip}")
                return None

            search_data = {}
            for dane in root.findall(".//dane"):
                for child in dane:
                    if child.text:
                        search_data[child.tag] = child.text

            report_data = self._get_full_report(regon)

            if report_data:
                merged_data = {**search_data, **report_data}
            else:
                merged_data = search_data

            if return_transformed:
                transformed_data = self._transform_result(merged_data)
                cache.set(cache_key, transformed_data, settings.GET_REGON_DATA_CACHE_TIMEOUT)
                return transformed_data

            return merged_data

        except Exception as e:
            self.logger.exception(e)
            return None
        finally:
            self._logout()

    def _get_full_report(self, regon: str) -> dict[str, Any] | None:
        """Get full report for entity by REGON."""
        try:
            client = self._get_client()

            # Determine report type based on REGON length
            if len(regon) == 9:
                report_name = "BIR11OsFizycznaDaneOgolne"
            elif len(regon) == 14:
                report_name = "BIR11JednLokalnaOsFizycznej"
            else:
                report_name = "BIR11OsPrawna"

            result = client.service.DanePobierzPelnyRaport(pRegon=regon, pNazwaRaportu=report_name)

            if not result or result == "":
                return None

            import xml.etree.ElementTree as ET

            root = ET.fromstring(result)  # noqa: S314 — BIR SOAP payload; defusedxml swap tracked as tech debt

            data = {}
            for child in root.iter():
                if child.text and child.tag != root.tag:
                    data[child.tag] = child.text

            return data

        except Exception as e:
            self.logger.exception(e)
            return None

    def _transform_result(self, result: dict[str, Any]) -> dict[str, Any]:
        """
        Transform REGON API response to common format compatible with other providers.

        Maps REGON API fields to the format used by gov_rejestr_wl_sdk.
        Supports both search result keys (Nazwa, Ulica) and full report keys (fiz_*, praw_*)
        """
        nazwa = (
            result.get("Nazwa")
            or result.get("fiz_nazwa")
            or result.get("praw_nazwa")
            or self._build_name_from_parts(result)
            or ""
        )

        data_zakonczenia = (
            result.get("DataZakonczeniaDzialalnosci")
            or result.get("fiz_dataSkresleniaPodmiotuZRegon")
            or result.get("praw_dataSkresleniaPodmiotuZRegon")
        )
        status_nip = "Nieczynny" if data_zakonczenia else "Czynny"

        return {
            "Nip": result.get("Nip") or result.get("fiz_nip") or result.get("praw_nip") or "",
            "Nazwa": nazwa,
            "StatusNip": status_nip,
            "Regon": result.get("Regon") or result.get("fiz_regon9") or result.get("praw_regon14") or "",
            "Ulica": result.get("Ulica") or result.get("fiz_adSiedzUlica") or result.get("praw_adSiedzUlica") or "",
            "NrNieruchomosci": result.get("NrNieruchomosci")
            or result.get("fiz_adSiedzNrNieruchomosci")
            or result.get("praw_adSiedzNrNieruchomosci")
            or "",
            "NrLokalu": result.get("NrLokalu")
            or result.get("fiz_adSiedzNrLokalu")
            or result.get("praw_adSiedzNrLokalu")
            or "",
            "Miejscowosc": result.get("Miejscowosc")
            or result.get("fiz_adSiedzMiejscowosc")
            or result.get("praw_adSiedzMiejscowosc")
            or "",
            "KodPocztowy": result.get("KodPocztowy")
            or result.get("fiz_adSiedzKodPocztowy")
            or result.get("praw_adSiedzKodPocztowy")
            or "",
            "MiejscowoscPoczty": result.get("MiejscowoscPoczty")
            or result.get("fiz_adSiedzMiejscowoscPoczty")
            or result.get("praw_adSiedzMiejscowoscPoczty")
            or "",
            "Wojewodztwo": result.get("Wojewodztwo")
            or result.get("fiz_adSiedzWojewodztwo_Nazwa")
            or result.get("praw_adSiedzWojewodztwo_Nazwa")
            or "",
            "Powiat": result.get("Powiat")
            or result.get("fiz_adSiedzPowiat_Nazwa")
            or result.get("praw_adSiedzPowiat_Nazwa")
            or "",
            "Gmina": result.get("Gmina")
            or result.get("fiz_adSiedzGmina_Nazwa")
            or result.get("praw_adSiedzGmina_Nazwa")
            or "",
            "DataZakonczeniaDzialalnosci": data_zakonczenia,
            "Typ": result.get("Typ") or ("F" if any(k.startswith("fiz_") for k in result.keys()) else "P"),
            "SilosID": result.get("SilosID") or "",
        }

    def _build_name_from_parts(self, result: dict[str, Any]) -> str:
        """Build full name from parts (nazwisko, imie1, imie2 for physical persons)."""
        nazwisko = result.get("fiz_nazwisko", "")
        imie1 = result.get("fiz_imie1", "")
        imie2 = result.get("fiz_imie2", "")

        parts = [p for p in [nazwisko, imie1, imie2] if p]
        return " ".join(parts) if parts else ""
