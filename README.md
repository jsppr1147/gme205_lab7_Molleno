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
