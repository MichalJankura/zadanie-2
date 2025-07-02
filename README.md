README

Tento repozitár obsahuje skript skrpti.py, ktorý sa dá spustiť manuálne aj automaticky pomocou GitHub Actions.

Predpoklady

Python 3.x

Sudo prístup pre inštaláciu závislostí (voliteľné)

Inštalácia

Klonujte repozitár:

git clone https://github.com/vas-uzivatel/vas-repo.git
cd vas-repo

(Voliteľné) Vytvorte a aktivujte virtuálne prostredie:

python3 -m venv venv
source venv/bin/activate

Nainštalujte požadované balíky (ak requirements.txt existuje):

pip install -r requirements.txt

Spustenie skriptu

Manuálne spustenie:

python skrpti.py

Automatické spúšťanie (GitHub Actions)

Skript sa spúšťa denne o 07:00 ráno, stredoeurópskeho času (CEST) pomocou workflow:

# .github/workflows/run-skrpti.yml
type: "schedule"
on:
  schedule:
    - cron: '0 5 * * *'  # 07:00 CEST = 05:00 UTC

jobs:
  run-skrpti:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.x'
      - run: python skrpti.py

Testovanie workflow

Ak chcete workflow otestovať okamžite, pridajte push event do on: alebo spustite prázdny commit:

git commit --allow-empty -m "Trigger workflow"
git push

V prípade otázok ma prosím kontaktujte.

