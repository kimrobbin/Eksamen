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
* Kan hende at du må kjøre denne kommandoen for å kunne koble til serveren
```bash
sudo nano /etc/mysql/mariadb.conf.d/50-server.cnf
# Så endre bind-adressen fra localhost/127.0.0.1 til 0.0.0.0
bind-address = 0.0.0.0

```
### 2. Avhengigheter

Installer nødvendige Python-pakker på local maskin:

```bash
pip install mysql-connector-python 
```
Note: getpass random hashlib er innebygd pakker 

### 3. Konfigurasjon

Oppdater database-tilkoblingsinnstillingene i `db.py` hvis nødvendig.

