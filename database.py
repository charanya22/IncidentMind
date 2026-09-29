from pathlib import Path
import duckdb

DB_PATH=Path("data/incidentmind.duckdb")

def get_connection():
    if not DB_PATH.exists():
        raise FileNotFoundError("Database not found. Run: python data_generator.py")
    return duckdb.connect(str(DB_PATH), read_only=True)

def get_incident(iid):
    con=get_connection()
    row=con.execute("SELECT * FROM incidents WHERE incident_id=?", [iid]).fetchdf()
    con.close()
    return None if row.empty else row.iloc[0].to_dict()

def _get(table,iid):
    con=get_connection()
    df=con.execute(f"SELECT * FROM {table} WHERE incident_id=?", [iid]).fetchdf()
    con.close()
    return df.to_dict("records")

def get_logs(iid): return _get("logs",iid)
def get_metrics(iid): return _get("metrics",iid)
def get_deployments(iid): return _get("deployments",iid)
def get_code_changes(iid): return _get("code_changes",iid)
def get_resolution(iid):
    rows=_get("resolutions",iid)
    return rows[0] if rows else None

def list_incidents():
    con=get_connection()
    df=con.execute("SELECT * FROM incidents ORDER BY incident_id").fetchdf()
    con.close()
    return df
