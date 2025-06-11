# KR Bank System

Et enkelt banksystem implementert i Python med MariaDB som database.

## Oppsett

### 1. Database Oppsett

Kjør følgende SQL-kommandoer for å sette opp database-brukeren:

```sql
CREATE USER 'bank'@'%' IDENTIFIED BY 'kimrobbin';
GRANT ALL PRIVILEGES ON KR_BANK.* TO 'bank'@'%';
FLUSH PRIVILEGES;
```

### 2. Avhengigheter

Installer nødvendige Python-pakker på local maskin:

```bash
pip install mysql-connector-python 
```
Note: getpass random hashlib er innebygd pakker 

### 3. Konfigurasjon

Oppdater database-tilkoblingsinnstillingene i `db.py` hvis nødvendig.

## Funksjoner

- Brukerregistrering og innlogging
- Opprette bankkontoer
- Sjekke saldo
- Overføre penger mellom kontoer

## Sikkerhet

- Passord blir hashet med SHA-256
- SQL-injection beskyttelse med parametriserte spørringer
- Kan ikke se passor i terminal