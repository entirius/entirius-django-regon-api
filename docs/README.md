# Django Regon API

## Introduction

Usługa udostępniania danych BIR1 jest częścią modułu Baza Internetowa Regon (BIR), który wchodzi
w skład zmodernizowanego systemu rejestru REGON. Usługa BIR1 udostępnia interfejs
programistyczny – zbiór metod, dzięki którym możliwe jest pobieranie danych z rejestru REGON
bezpośrednio z systemu zewnętrznego. Zasadniczą funkcjonalnością usługi jest udostępnianie danych,
osobom fizycznym oraz podmiotom komercyjnym.

## Configuration

W settings należy ustawić zienne:
BIR_API_KEY -> klucz użytkownika 
BIR_SERVICE_URL -> url który wykorzystujemy w regon-sdk
BIR_WSDL_URL -> wsdl który wykorzystujemy w regon-sdk
BIR_VERSIONS -> wersja usługi, której chcemy użyć obecnie dostępne są bir1 oraz bir1.1


## Test BIR 1.1

Klucz użytkownika (testowy): abcde12345abcde12345

## Production BIR 1.1

W celu uzyskania klucza użytkownika dla środowiska produkcyjnego prosimy o przesłanie
wniosku w postaci zwykłej wiadomości email na adres regon_bir@stat.gov.pl zawierającego
następujące informacje:

* pełna nazwa podmiotu;
* numer REGON podmiotu (lub numer NIP dla osób nie prowadzących działalności gosp.)
* imię i nazwisko osoby do kontaktu;
* adres email osoby do kontaktu;
* numer telefonu stacjonarny;
* (i/lub) numer telefonu komórkowy;
* przybliżona liczba użytkowników końcowych, którzy będą jednocześnie korzystać z Usługi.
(Równoważne liczbie jednocześnie uruchomionych instancji aplikacji na stacjach roboczych
lub innych urządzeniach końcowych jednocześnie korzystających z Usługi).
* adresy IP, z których będą się komunikowały Państwa systemy teleinformatyczne. (Dotyczy
sytuacji gdy użytkownicy końcowi będą łączyć się z BIR1 poprzez serwer dostępowy dostawcy
oprogramowania -punkt 3.6.3 "Instrukcji technicznej" pt. "Zalecana architektura"). Ponadto,
gdy adres/pula adresów IP jest stała - zalecamy podanie tych adresów dla celów
diagnostycznych (w przypadku ew. kłopotów z korzystaniem z Usługi).

```text
Uwaga!
Przesłanie powyższego formularza z danymi jest równoznaczne ze zgodą na przetwarzanie danych
osoby do kontaktu oraz zgodą na otrzymywanie powiadomień dot. przerw technicznych oraz ew.
zmian w Usłudze. Administratorem danych osobowych jest Prezes GUS. Więcej pod adresem:
http://bip.stat.gov.pl/rodo/klauzule-informacyjne/zamowienie-na-dane-statystyczne/
```

## Usage

Uderzając pod konkretny endpoint z numerem NIP/REGON/KRS otrzymamy dane o firmie. Dane zostaną zapisane w folderze *data>bir*
Adresy są dostępne w pliku **bir1.md** w folderze *docs>api*

