# Bir1

## GET data by NIP

Zwraca zestaw danych dotyczących klienta z bazy GUS

Przykladowa odpowiedź:

```text
"data": [
{
"Regon": "1234500789",
"Nip": "73428007148",
"StatusNip": "",
"Nazwa": "NAZWA",
"Wojewodztwo": "WOJEWÓDZTWO",
"Powiat": "POWIAT",
"Gmina": "GMINA",
"Miejscowosc": "MIEJSCOWOSC",
"KodPocztowy": "00-000",
"Ulica": "ul. Ulica",
"NrNieruchomosci": "00",
"NrLokalu": "",
"Typ": "P",
"SilosID": "00",
"DataZakonczeniaDzialalnosci": "",
"MiejscowoscPoczty": "MIEJSCOWOSC"
}
]
```

`api/regon/V1/bir1/nip/<str:nip>/`

## GET data by KRS

Zwraca zestaw danych dotyczących klienta z bazy GUS


Przykladowa odpowiedź:

```text
"data": [
{
"Regon": "1234500789",
"Nip": "12345007890",
"StatusNip": "",
"Nazwa": "NAZWA",
"Wojewodztwo": "WOJEWÓDZTWO",
"Powiat": "POWIAT",
"Gmina": "GMINA",
"Miejscowosc": "MIEJSCOWOSC",
"KodPocztowy": "00-000",
"Ulica": "ul. Ulica",
"NrNieruchomosci": "00",
"NrLokalu": "",
"Typ": "P",
"SilosID": "00",
"DataZakonczeniaDzialalnosci": "",
"MiejscowoscPoczty": "MIEJSCOWOSC"
}
]
```

`api/regon/V1/bir1/krs/<str:krs>/`

## GET data by REGON

Zwraca zestaw danych dotyczących klienta z bazy GUS


Przykladowa odpowiedź:

```text
"data": [
{
"Regon": "1234500789",
"Nip": "73428007148",
"StatusNip": "",
"Nazwa": "NAZWA",
"Wojewodztwo": "WOJEWÓDZTWO",
"Powiat": "POWIAT",
"Gmina": "GMINA",
"Miejscowosc": "MIEJSCOWOSC",
"KodPocztowy": "00-000",
"Ulica": "ul. Ulica",
"NrNieruchomosci": "00",
"NrLokalu": "",
"Typ": "P",
"SilosID": "00",
"DataZakonczeniaDzialalnosci": "",
"MiejscowoscPoczty": "MIEJSCOWOSC"
}
]
```

`api/regon/V1/bir1/regon/<str:regon>/`

## GET reports by REGON

Zwraca grupę raportów z bazy BIR1

Przykładowa odpowiedź:

```text
"data": {
BIR11OsFizycznaPkd": [
{
    "fiz_pkd_Kod": "6201Z",
    "fiz_pkd_Nazwa": "DZIAŁALNOŚĆ ZWIĄZANA Z OPROGRAMOWANIEM",
    "fiz_pkd_Przewazajace": "1",
    "fiz_SilosID": "6",
    "fiz_Silos_Symbol": "Prawna",
    "fiz_dataSkresleniaDzialalnosciZRegon": ""
},
[...]
{
    "fiz_pkd_Kod": "0129Z",
    "fiz_pkd_Nazwa": "UPRAWA POZOSTAŁYCH ROŚLIN WIELOLETNICH",
    "fiz_pkd_Przewazajace": "0",
    "fiz_SilosID": "6",
    "fiz_Silos_Symbol": "Prawna",
    "fiz_dataSkresleniaDzialalnosciZRegon": ""
},
]
}
```
`api/regon/V1/bir1/repotrs/<str:regon>/`
