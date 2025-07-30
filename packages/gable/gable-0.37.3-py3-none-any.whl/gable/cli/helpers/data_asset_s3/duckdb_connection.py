import threading
import duckdb

_thread_local = threading.local()

def get_duckdb_connection():
    """Get a thread-local DuckDB connection with extensions loaded."""
    if not hasattr(_thread_local, 'duckdb_conn'):
        _thread_local.duckdb_conn = duckdb.connect()
        _thread_local.duckdb_conn.query("INSTALL httpfs; LOAD httpfs;")
        _thread_local.duckdb_conn.query("CREATE OR REPLACE SECRET secret (TYPE s3,PROVIDER credential_chain);")
        # _thread_local.duckdb_conn.query("INSTALL orc;   LOAD orc;")  # load ORC extension only if used
    return _thread_local.duckdb_conn