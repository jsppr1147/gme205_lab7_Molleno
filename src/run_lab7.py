import json

from database import fetch_parcels_by_land_use
from exchange import build_feature_collection, validate_feature_collection
from spatial import Parcel

rows = fetch_parcels_by_land_use("Residential")
print("Rows returned:", len(rows))

parcels = [
    Parcel.from_row(row)
    for row in rows
]
print("Parcel objects created:", len(parcels))

collection = build_feature_collection(parcels)
print("GeoJSON type:", collection["type"])
print("Feature count:", len(collection["features"]))

if collection["features"]:
    print(
        "First feature:",
        json.dumps(
            collection["features"][0],
            indent=2,
        ),
    )
# Uncomment the following line to test a failing case for the GeoJSON contract validation    
#collection["features"][0]["id"] = None
try:
    validate_feature_collection(collection)
    print("GeoJSON contract check: PASSED")
except ValueError as error:
    print("GeoJSON contract check: FAILED")
    print(error)