import psycopg2 as postgres
from psycopg2 import sql


def get_connection():
    return postgres.connect(
        host="localhost",
        port=5432,
        user="postgres",
        password="FreezeStainCool4"
    )
    
def create_and_verify_db():
    
    con = get_connection()
    con.autocommit = True
    cursor = con.cursor()
    
    db_name = "file hashes"
    cursor.execute(sql.SQL("SELECT 1 FROM pg_database WHERE datname = %s"), [db_name])
    exists = cursor.fetchone()

    if not exists:
        cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name)))
    else:
        print("database not made")
        
    cursor.close()
    con.close()
    

def create_and_verify_table():
    con = get_connection()
    cursor = con.cursor()
    
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS file_hashes_table(
                id SERIAL PRIMARY KEY,
                filepath TEXT UNIQUE NOT NULL,
                filehash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """)
    
    cursor.close()
    con.close()

# returns filepath hash
def get_baseline(filepath:str):
    # validate that it's str first, 
    con = get_connection()
    cursor = con.cursor()
    cursor.execute(sql.SQL("SELECT * FROM file_hashes_table WHERE filepath = %s"),  [str(filepath)])
    
    value = cursor.fetchone()
    
    con.close()
    cursor.close()
    
    if value:
        return value
        
    else:
        return "UNKNOWN"


# returns dict
def get_all_baseline_values():
    loaded_baselines = {}
    
    con = get_connection()
    cursor = con.cursor()
    cursor.execute(sql.SQL("SELECT filepath, filehash FROM file_hashes_table"))
    
    for filepath, filehash in cursor.fetchall():
        loaded_baselines[filepath] = filehash    
    
    con.close()
    cursor.close()
    return loaded_baselines


# clears db, should require second level of auth
# for some reason works in cli but not here
def clear_baseline():
    con = get_connection()
    cursor = con.cursor()
    cursor.execute("TRUNCATE TABLE file_hashes_table;")
    con.commit()
    
    cursor.close()
    con.close()
    

def add_entry(file_path:str, file_hash:str):
    # verify file_path is of type str
    con = get_connection()
    cursor = con.cursor()
    
    cursor.execute("""
    INSERT INTO file_hashes_table (filepath, filehash)
    VALUES (%s, %s);
""", (str(file_path), file_hash))
    
    con.commit()
    
    
def update_entry(filepath, new_filehash):
    pass
    

if __name__ == "__main__":
    print(get_all_baseline_values())