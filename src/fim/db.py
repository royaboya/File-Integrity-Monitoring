from contextlib import contextmanager
import psycopg2 as postgres
from psycopg2 import sql
from config import HOST, PGSQL_PORT, PGSQL_PW, PGSQL_USER

# need to add str checking for p

def get_connection():
    return postgres.connect(
        host=HOST,
        port=PGSQL_PORT,
        user=PGSQL_USER,
        password=PGSQL_PW
    )

# context manager to handle creating and closing connections
@contextmanager
def db_cursor_conn():
    with get_connection() as con:
        with con.cursor() as cur:
            yield cur
    

def create_and_verify_db():
    with db_cursor_conn() as cur:
        cur.connection.autocommit = True
        db = "file hashes"
        cur.execute(sql.SQL("SELECT 1 FROM pg_database WHERE datname = %s"), [db])
        
        exists = cur.fetchone()
        
        if not exists:
            cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db)))
        else:
            print("DB not made") # change this
        
    

def create_and_verify_table():
    with db_cursor_conn as cur:
        cur.execute("""
                CREATE TABLE IF NOT EXISTS file_hashes_table(
                    id SERIAL PRIMARY KEY,
                    filepath TEXT UNIQUE NOT NULL,
                    filehash TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                """)
        cur.connecton.commit()

# returns filepath hash
def get_baseline(filepath:str):
    # validate that it's str first, 
    with db_cursor_conn as cur:
        cur.execute(sql.SQL("SELECT * FROM file_hashes_table WHERE filepath = %s"),  [str(filepath)])
        value = cur.fetchone()
    
    if value:
        return value
        
    else:
        return "UNKNOWN"


# returns dict
def get_all_baseline_values():
    loaded_baselines = {}
    with db_cursor_conn as cur:
        cur.execute(sql.SQL("SELECT filepath, filehash FROM file_hashes_table"))
    
        for filepath, filehash in cur.fetchall():
            loaded_baselines[filepath] = filehash    

    return loaded_baselines


# clears db, should require second level of auth
def clear_baseline():
    with db_cursor_conn() as cur:
        cur.execute("TRUNCATE TABLE file_hashes_table;")
        cur.connection.commit()    

def add_entry(file_path:str, file_hash:str):
    # verify file_path is of type str
    with db_cursor_conn() as cur:
        cur.execute("""
            INSERT INTO file_hashes_table (filepath, filehash)
            VALUES (%s, %s);
            """, (str(file_path), file_hash))
        cur.connection.commit()
    
def add_bulk_entries(file_hash_records):
    with db_cursor_conn() as cur:
        cur.executemany("""
                INSERT INTO file_hashes_table (filepath, filehash) 
                VALUES (%s, %s) ON CONFLICT (filepath) DO UPDATE SET filehash = EXCLUDED.filehash
                """, file_hash_records)
        cur.connection.commit()
    

# add on-conflict handling
def update_entry(filepath, new_filehash):
    with db_cursor_conn() as cur:
        cur.execute(
            """
            UPDATE file_hashes_table
            SET filehash = %s
            WHERE filepath = %s
            """, (new_filehash, filepath))
        cur.connection.commit()
    

if __name__ == "__main__":
    print(get_all_baseline_values())