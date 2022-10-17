from ast import Str
import psycopg2

def create_db(conn):
    with conn.cursor() as cur:
        cur.execute('''
        CREATE TABLE IF NOT EXISTS clients(
        id SERIAL PRIMARY KEY,
        name VARCHAR(40),
        surname VARCHAR(40),
        email VARCHAR(40)
        );
        ''')
        
        cur.execute('''
        CREATE TABLE IF NOT EXISTS phones(
        phone_id SERIAL PRIMARY KEY,
        phone_number VARCHAR(15) UNIQUE,
        client_id INT4 REFERENCES clients(id)
        );
        ''')
        conn.commit()

def add_client(conn, name: str, surname: str, email: str):
    with conn.cursor() as cur:
        cur.execute(f"INSERT INTO clients(name, surname, email) VALUES ('{name}', '{surname}', '{email}')")
        conn.commit()
        

def add_phone(conn, client_id: int, phone: str):
    with conn.cursor() as cur:
        cur.execute(f"INSERT INTO phones(phone_number, client_id) VALUES ('{phone}', '{client_id}')")
        conn.commit()

def change_client(conn, client_id, name=None, surname=None, email=None):
    if name or surname or email:    
        set_part = 'SET ' + ','.join([['', f"name = '{name}'"][bool(name)], 
                                     ['', f"surname = '{surname}'"][bool(surname)],
                                     ['', f"email = '{email}'"][bool(email)]])
    with conn.cursor() as cur:
        cur.execute(f'''
        UPDATE clients
        {set_part}
        WHERE id = {client_id};
                    ''')
        conn.commit()

def delete_phone(conn, client_id, phone):
    with conn.cursor() as cur:
        cur.execute(f'''
        DELETE FROM phones
        WHERE phone_number = '{phone}' AND client_id = '{client_id}';
        ''')
        conn.commit()

def delete_client(conn, client_id):
    with conn.cursor() as cur:
        cur.execute(f'''
        DELETE FROM phones
        WHERE client_id = '{client_id}';
        ''')
        cur.execute(f'''
        DELETE FROM clients
        WHERE id = '{client_id}';
        ''')
        conn.commit()

def find_client(conn, name=None, surname=None, email=None, phone=None):
    with conn.cursor() as cur:
        cur.execute(f'''
        SELECT c.name, c.surname, c.email, p.phone_number FROM clients c
        JOIN phones p on p.client_id = c.id
        WHERE c.name = '{name}' OR c.surname = '{surname}' OR c.email = '{email}' OR p.phone_number = '{phone}';
                    ''')
        return cur.fetchone()

with open('password.txt') as pw:
    password = pw.read()
    
with psycopg2.connect(database="shop_info", user="postgres", password=password) as conn:
    create_db(conn)
    #add_client(conn, 'William', 'Butcher', 'wbutcher@google.com')
    #add_phone(conn, 2, '88005553535')
    #change_client(conn, 1, 'Will', 'Smith', 'WSmith@Hollywood.us')
    #delete_phone(conn, 1, '88005553535')
    #delete_client(conn, 1)
    print(find_client(conn=conn, email='wbutcher@google.com'))
conn.close()