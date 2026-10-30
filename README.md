Gme 205 Lab 7: Python-PostGIS to Interoperable JSON

## commit logs  

PART A:  Setup and database check  
- Created the project structure: `src/` (database.py, spatial.py, exchange.py, run_lab7.py) and `output/`
- Created `.venv` and installed psycopg[binary] and python-dotenv; saved to `requirements.txt`
- Created `.env.example`; added `.env` to `.gitignore`
- `lab6.parcels` has P-001 to P-004: <added using the seed SQL> 

Part B: Connecting and Writing a parametrize function  
- Implemented `DB_CONFIG`, `check_connection()`, and `fetch_parcels_by_land_use()` in `src/database.py`
- updated run_lab7.py for connection checking.
- Connection check: <result>
    > Connection successful.  
    > Database: gme205  
    > PostGIS: 3.6 USE_GEOS=1 USE_PROJ=1 USE_STATS=1  
- updated run_lab7.py for land_use query
- Query for "Residential" returned 2 rows
- First row: P-001, Residential, polygon transformed to EPSG:4326 (lon ≈ 118.511, lat ≈ 0)
- land_use is passed as a separate parameter (`%s`), not inserted into the SQL text  

Part C: Converting Rows to PArcel
 - Implemented the `Parcel` class in `src/spatial.py` with `from_row()` and `to_feature()`  
- `from_row()` converts the GeoJSON string in the row into a Python dict  
- 2 database rows converted into 2 Parcel objects  
- First object: P-001, Residential  

Part D: Creating GeoJSON Exchange 
- Implemented `build_feature_collection()` and `validate_feature_collection()` in `src/exchange.py`
- FeatureCollection built with 2 features
- Contract check:
    - PASSED
    First feature: {
        "type": "Feature",
        "id": "P-001",
        "geometry": {
            "type": "Polygon",
            "coordinates": [[[
          118.511256116,
          0],
        [
          118.512152016,
          0
        ],
        [
          118.512152015,
          0.000901939
        ],
        [
          118.511256115,
          0.000901938
        ],
        [
          118.511256116,
          0
        ]]]},
        "properties": {
            "parcel_id": "P-001",
            "land_use": "Residential"}}
    GeoJSON contract check: PASSED

- Also,tested the validator by removing a feature id: it raised "Feature is missing id".
    - Failed
    Rows returned: 2
    Parcel objects created: 2
    GeoJSON type: FeatureCollection
    Feature count: 2
    First feature: {
        "type": "Feature",
        "id": "P-001",
        "geometry": {
            "type": "Polygon",
            "coordinates": [[[
          118.511256116,
          0
        ],
        [
          118.512152016,
          0
        ],
        [
          118.512152015,
          0.000901939
        ],
        [
          118.511256115,
          0.000901938
        ],
        [
          118.511256116,
          0]]]},
          "properties": {
            "parcel_id": "P-001",
            "land_use": "Residential"}}
    GeoJSON contract check: FAILED
    Feature is missing id  

Part E: Integrating the Workflow and Writing the output
- Completed `src/run_lab7.py` as the workflow runner: connection → query → objects → FeatureCollection → validation → file
- Generated `output/residential_parcels.geojson` with 2 features (P-001, P-002)
- Loaded the file in QGIS: yes. Screenshot located in output/QGIS_input.png

"""
Connection successful.
Database: gme205
PostGIS: 3.6 USE_GEOS=1 USE_PROJ=1 USE_STATS=1
Rows returned: 2
First database row: ('P-001', 'Residential', '{"type":"Polygon","coordinates":[[[118.511256116,0],[118.512152016,0],[118.512152015,0.000901939],[118.511256115,0.000901938],[118.511256116,0]]]}')
Parcel objects created: 2
First Parcel object: P-001 Residential
GeoJSON type: FeatureCollection
Feature count: 2
GeoJSON contract check: PASSED
Output written: output\residential_parcels.geojson
File exists: True
"""

Part F: Reflections

1. The database handles the spatial work and filtering. It selects matching rows by land use, transforms coordinates to EPSG:4326 using ST_Transform, and formats them as GeoJSON with ST_AsGeoJSON. Python just gets clean results and does not need to handle raw geometry types.

2. Using parameterized queries (%s) passes the filter value separately from the SQL statement. The database treats the input purely as plain data, preventing SQL injection and avoiding syntax crashes if a string contains quotes or special characters. F-strings directly inject raw text into the query, leaving it vulnerable. 

3. Executing a query returns a raw tuple which forces the user to reference fields by index (row[0]). Mapping it into a Parcel class assigns explicit property names (parcel_id, land_use, geometry) and parses the raw JSON geometry string into a native Python dictionary.

4. The method reformats the Parcel instance into standard GeoJSON schema (type, id, geometry, properties). This creates a universal JSON dictionary that external web maps or GIS applications can read without knowing anything about the Parcel class.

5. The database keeps spatial data in its local metric projection (UTM Zone 51N / EPSG:32651) for accurate measurements. The GeoJSON specification (RFC 7946) requires coordinates in WGS 84 (EPSG:4326), so transforming the data on export ensures compliance while keeping the stored spatial data intact.

6. Interoperability means external applications can process your data without needing to know your database schema or backend code. Since GeoJSON is an open industry standard, software like QGIS can render the exported file directly, whether it's downloaded locally or served over an API.