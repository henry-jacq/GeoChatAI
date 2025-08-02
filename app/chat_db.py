import sqlite3
import uuid

DB_PATH = "chat_data.db"


def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chats (
                chat_id TEXT PRIMARY KEY,
                chat_title TEXT,
                image_name TEXT,
                response_txt TEXT,
                is_streamed INTEGER DEFAULT 0
            )
        ''')
        conn.commit()


def add_chat(chat_title, image_name, response_txt, is_streamed=False):
    chat_id = str(uuid.uuid4())
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO chats (chat_id, chat_title, image_name, response_txt, is_streamed)
            VALUES (?, ?, ?, ?, ?)
        ''', (chat_id, chat_title, image_name, response_txt, int(is_streamed)))
        conn.commit()
    return chat_id


def get_chat(chat_id):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM chats WHERE chat_id = ?', (chat_id,))
        return cursor.fetchone()


def get_all_chats():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            'SELECT chat_id, chat_title FROM chats ORDER BY rowid DESC')
        return cursor.fetchall()


def update_chat_response(chat_id, response_txt, is_streamed=None):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        if is_streamed is not None:
            cursor.execute('''
                UPDATE chats
                SET response_txt = ?, is_streamed = ?
                WHERE chat_id = ?
            ''', (response_txt, int(is_streamed), chat_id))
        else:
            cursor.execute('''
                UPDATE chats
                SET response_txt = ?
                WHERE chat_id = ?
            ''', (response_txt, chat_id))
        conn.commit()
