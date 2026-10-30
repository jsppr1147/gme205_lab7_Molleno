from database import fetch_parcels_by_land_use

rows = fetch_parcels_by_land_use("Residential")
print("Rows returned:", len(rows))
if rows:
    print("First database row:", rows[0])