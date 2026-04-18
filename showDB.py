import sqlite3

def print_all_data(table_name):
    try:
        conn = sqlite3.connect('chat.db')
        cursor = conn.cursor()

        cursor.execute(f"SELECT * FROM {table_name}")
        
        column_names = [description[0] for description in cursor.description]
        print(f"Таблица: {table_name}")
        print(column_names)
        print("-" * 60)

        rows = cursor.fetchall()
        for row in rows:
            print(row)

    except sqlite3.Error as e:
        print(f"Ошибка при работе с SQLite: {e}")
    finally:
        if conn:
            conn.close()

print_all_data('messages')
