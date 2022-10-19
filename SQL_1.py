import psycopg2

def create_db(conn):
    with conn.cursor() as cur:
        cur.execute('''
        CREATE TABLE IF NOT EXISTS clients(
        id SERIAL PRIMARY KEY,
        name VARCHAR(40) NOT NULL,
        surname VARCHAR(40) NOT NULL,
        email VARCHAR(40) NOT NULL);
        ''')
        
        cur.execute('''
        CREATE TABLE IF NOT EXISTS phones(
        phone_id SERIAL PRIMARY KEY,
        phone_number VARCHAR(15) UNIQUE,
        client_id INT4 REFERENCES clients(id));
        ''')
        conn.commit()
        return 'Таблицы успешно добавлены'

def add_client(conn):
    name = input('Введите имя клиента : ')
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
    name = input('Введите имя клиента (нажмите Enter для пропуска): ')
    surname = input('Введите фамилию клиента (нажмите Enter для пропуска): ')
    email = input('Введите email клиента (нажмите Enter для пропуска): ') 
    set_part = 'SET '
    for i, info in enumerate([name, surname, email]):
        if info:
            set_part = set_part + ['name=', 'surname=', 'email='][i] + "'" + info + "'"
    set_part = set_part.strip(',')
    if name or surname or email:             
        with conn.cursor() as cur:
            cur.execute(f'''
            UPDATE clients
            {set_part}
            WHERE id = {client_id};
            ''')
            conn.commit()
        return f'Данные клиента с id {client_id} успешно изменены'
    else:
        print('Данных для изменения не введено')

def delete_phone(conn):
    client_id = int(input('Введите ID клиента: '))
    phone = input('Введите номер телефона: ')
    with conn.cursor() as cur:
        cur.execute(f'''
        DELETE FROM phones
        WHERE phone_number = '{phone}' AND client_id = '{client_id}'
        RETURNING phone_id;
        ''')
        result = cur.fetchone()
        conn.commit()
    if result == None:
        return 'Такого номера телефона не найдено'
    else:
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
        WHERE id = '{client_id}'
        RETURNING id;
        ''')
        result = cur.fetchone()
        conn.commit()
    if result == None:
        return 'Такого клиента в базе не найдено'
    else:
        return f'Клиент с id {client_id} успешно удален'

def find_client(conn):
    name = input('Введите имя клиента (нажмите Enter для пропуска): ')
    surname = input('Введите фамилию клиента (нажмите Enter для пропуска): ')
    email = input('Введите email клиента (нажмите Enter для пропуска): ')
    phone = input('Введите номер телефона (нажмите Enter для пропуска): ')
    with conn.cursor() as cur:
        cur.execute(f'''
        SELECT a.id, a.name, a.surname, a.email FROM (select * from clients left join phones on phones.client_id = clients.id) as a
        WHERE a.name = '{name}' OR a.surname = '{surname}' OR a.email = '{email}' OR a.phone_number = '{phone}';
                    ''')
        conn.commit()
        result = cur.fetchone()
    if result:
        return f'''Данные о клиенте:
                id = {result[0]}
                Имя = {result[1]}
                Фамилия = {result[2]}
                email = {result[3]}
                '''
    else:
        return 'Данных о клиенте не найдено'

def get_phones(conn):
    client_id = int(input('Введите ID клиента: '))
    with conn.cursor() as cur:
        cur.execute(f'''
        SELECT a.phone_number FROM (select * from clients left join phones on phones.client_id = clients.id) as a
        WHERE a.client_id = '{client_id}';
                    ''')
        
        conn.commit()
        result = cur.fetchall()
    if result:
        return '\n'.join([number[0] for number in result])
    else:
        return 'Телефонных номеров у клиента не обнаружено'
    
def get_help(conn):
    print('''Список доступных команд:
          create db - создает таблицы clients и phones
          add client - добавляет нового клиента
          add phone - добавляет номер телефона существующему клиенту (по client_id)
          change client - изменяет данные о клиенте (имя, фамилию или email)
          delete phone - удаляет номер телефона клиента
          delete client - удалает клиента из базы
          find client - выдает информацию о клиенте по имени, фамилии, email или номеру телефона
          get phones - показывает, какие номера телефонов привязаны к клиенту
          exit - выход из программы''')
    
def start_database_manager(): 
    with open('password.txt') as pw:
        password = pw.read()
    with psycopg2.connect(database="shop_info", user="postgres", password=password) as conn:
        func_choice = {'create db': create_db, 'add client': add_client, 'add phone': add_phone, 'change client': change_client, 
                    'delete phone': delete_phone, 'delete client': delete_client, 'find client': find_client, 'get phones': get_phones,
                    'help': get_help, 'exit': 'exit'}
        chosen_option = ''
        while chosen_option != 'exit':
            chosen_option = input('Введите команду: ')
            if chosen_option == 'exit':
                print('Работа программы завершена')
                continue
            try:
                print(func_choice[chosen_option](conn))
            except KeyError:
                print('Неверно набрана команда')
    conn.close()
    
if __name__ == '__main__':
    start_database_manager()