import sqlite3


def init_db():
    conn = sqlite3.connect('flappy_bird.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS scores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        player_name TEXT,
        score INTEGER
    )
    ''')
    conn.commit()
    conn.close()


def save_score(player_name, score):
    conn = sqlite3.connect('flappy_bird.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO scores (player_name, score) VALUES (?, ?)', (player_name, score))
    conn.commit()
    conn.close()


def get_scores():
    conn = sqlite3.connect('flappy_bird.db')
    cursor = conn.cursor()
    cursor.execute('SELECT player_name, score FROM scores ORDER BY score DESC')
    scores = cursor.fetchall()
    conn.close()
    return scores
