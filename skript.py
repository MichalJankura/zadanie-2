import os
import requests
import psycopg2
from dotenv import load_dotenv

# Načítanie environment premenných
load_dotenv()
# Golemio API kľúč a URL kluc by mal byt v .env s
API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Mzc0OSwiaWF0IjoxNzUxMjg5NjI2LCJleHAiOjExNzUxMjg5NjI2LCJpc3MiOiJnb2xlbWlvIiwianRpIjoiYTAzZjM1YjYtMjZiNi00OWYwLTg5N2EtMjEwMzUyN2ZjOThmIn0.8qushmXU3wceT2Sfm_TYWSu8YW8hRWq4-ixWKZjj6Ms"

API_URL = "https://api.golemio.cz/v2/municipalLibraries"

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "2-zadanie")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "toor")


def fetch_libraries():
    headers = {"x-access-token": API_KEY}
    response = requests.get(API_URL, headers=headers)
    response.raise_for_status()
    return response.json().get("features", [])


def extract_library_info(lib):
    properties = lib["properties"]
    addr = properties["address"]
    coords = lib["geometry"]["coordinates"]

    opening_hours = []
    for entry in properties.get("opening_hours", []):
        opening_hours.append(
            f'{entry["day_of_week"]}: {entry["opens"]}–{entry["closes"]} ({entry["description"]})'
        )

    return {
        "id": properties["id"],
        "name": properties["name"],
        "street": addr.get("street_address"),
        "postal_code": addr.get("postal_code"),
        "city": addr.get("address_locality"),
        "region": properties.get("district"),
        "country": addr.get("address_country"),
        "latitude": coords[1],
        "longitude": coords[0],
        "opening_hours": "; ".join(opening_hours)
    }

#Tieto udaje sa davaju do .env suboru ale kedze ide len o zadanie tak ponechavam sem
def insert_into_postgres(records):
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )
    cur = conn.cursor()

    # Vloženie dát do tabuľky
    insert_sql = """
        INSERT INTO kniznice (
            id_kniznice, nazov_kniznice, ulica, psc, mesto, kraj,
            krajina, zemepisna_sirka, zemepisna_dlzka, cas_otvorenia
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (id_kniznice) DO UPDATE SET
            nazov_kniznice = EXCLUDED.nazov_kniznice,
            ulica = EXCLUDED.ulica,
            psc = EXCLUDED.psc,
            mesto = EXCLUDED.mesto,
            kraj = EXCLUDED.kraj,
            krajina = EXCLUDED.krajina,
            zemepisna_sirka = EXCLUDED.zemepisna_sirka,
            zemepisna_dlzka = EXCLUDED.zemepisna_dlzka,
            cas_otvorenia = EXCLUDED.cas_otvorenia;
    """


    for rec in records:
        cur.execute(insert_sql, (
            rec["id"],
            rec["name"],
            rec["street"],
            rec["postal_code"],
            rec["city"],
            rec["region"],
            rec["country"],
            rec["latitude"],
            rec["longitude"],
            rec["opening_hours"]
        ))

    conn.commit()
    cur.close()
    conn.close()


def main():
    print("Načítavam dáta z Golemio API...")
    libs = fetch_libraries()
    extracted = [extract_library_info(lib) for lib in libs]
    print(f"Získaných {len(extracted)} záznamov. Vkladám do databázy...")
    insert_into_postgres(extracted)
    print("Hotovo.")


if __name__ == "__main__":
    main()
