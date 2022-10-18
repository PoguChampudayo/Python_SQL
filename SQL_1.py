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
        return 'Таблицы успешно добавлены'

def add_client(conn):
    name = input('Введите имя клиента: ')
    surname = input('Введите фамилию клиента: ')
    email = input('Введите email клиента: ')
    with conn.cursor() as cur:
        cur.execute(f"INSERT INTO clients(name, surname, email) VALUES ('{name}', '{surname}', '{email}')")
        conn.commit()
    return f'Клиент {name} {surname} успешно добавлен'
        

def add_phone(conn):
    client_id = int(input('Введите ID клиента: '))
    phone = input('Введите номер телефона: ')
    with conn.cursor() as cur:
        cur.execute(f"INSERT INTO phones(phone_number, client_id) VALUES ('{phone}', '{client_id}')")
        conn.commit()
    return f'Номер телефона {phone} успешно добавлен'

def change_client(conn):
    client_id = int(input('Введите ID клиента: '))
    name = input('Введите имя клиента: ')
    surname = input('Введите фамилию клиента: ')
    email = input('Введите email клиента: ')
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
    return f'Данные клиента с id {client_id} успешно изменены'

def delete_phone(conn):
    client_id = int(input('Введите ID клиента: '))
    phone = input('Введите номер телефона: ')
    with conn.cursor() as cur:
        cur.execute(f'''
        DELETE FROM phones
        WHERE phone_number = '{phone}' AND client_id = '{client_id}';
        ''')
        conn.commit()
    return f'Номер телефона {phone} успешно удален'

def delete_client(conn):
    client_id = int(input('Введите ID клиента: '))
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
    return f'Клиент с id {client_id} успешно удален'

def find_client(conn):
    name = input('Введите имя клиента: ')
    surname = input('Введите фамилию клиента: ')
    email = input('Введите email клиента: ')
    phone = input('Введите номер телефона: ')
    with conn.cursor() as cur:
        cur.execute(f'''
        SELECT c.id, c.name, c.surname, c.email, p.phone_number FROM clients c
        JOIN phones p on p.client_id = c.id
        WHERE c.name = '{name}' OR c.surname = '{surname}' OR c.email = '{email}' OR p.phone_number = '{phone}';
                    ''')
        result = cur.fetchone()
    return f'''Данные о клиенте:
id = {result[0]}
Имя = {result[1]}
Фамилия = {result[2]}
email = {result[3]}
Номер телефона = {result[4]}'''

def get_help():
    print('''Список доступных команд:
          create db - создает таблицы clients и phones
          add client - добавляет нового клиента
          add phone - добавляет номер телефона существующему клиенту (по client_id)
          change client - изменяет данные о клиенте (имя, фамилию или email)
          delete phone - удаляет номер телефона клиента
          delete client - удалает клиента из базы
          find client - выдает информацию о клиенте по имени, фамилии, email или номеру телефона
          exit - выход из программы''')
with open('password.txt') as pw:
    password = pw.read()


with psycopg2.connect(database="shop_info", user="postgres", password=password) as conn:
    func_choice = {'create db': create_db(conn), 'add client': add_client(conn), 'add phone': add_phone(conn), 'change client': change_client(conn), 
                   'delete phone': delete_phone(conn), 'delete client': delete_client(conn), 'find client': find_client(conn), 'help': get_help(), 'exit': 'exit'}
    chosen_option = ''
    while chosen_option != 'exit':
        chosen_option = input('Введите команду: ')
        print(func_choice[chosen_option])
    
   # create_db(conn)
    #add_client(conn, 'William', 'Butcher', 'wbutcher@google.com')
    #add_phone(conn, 2, '88005553535')
    #change_client(conn, 1, 'Will', 'Smith', 'WSmith@Hollywood.us')
    #delete_phone(conn, 1, '88005553535')
    #delete_client(conn, 1)
    #print(find_client(conn=conn, email='wbutcher@google.com'))
conn.close()