import sqlite3


def add_player(name):
    conn = sqlite3.connect("players.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS players (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT UNIQUE,
                        best_score INTEGER DEFAULT 0,
                        best_time REAL DEFAULT 0.0,
                        coins INTEGER DEFAULT 0
                    )''')
    try:
        cursor.execute("INSERT INTO players (name) VALUES (?)", (name,))
        conn.commit()
    except sqlite3.IntegrityError:
        pass  # Игрок уже есть
    conn.close()


def update_player(name, score, time, coins):
    conn = sqlite3.connect("players.db")
    cursor = conn.cursor()

    cursor.execute("SELECT best_score, best_time, coins FROM players WHERE name = ?", (name,))
    result = cursor.fetchone()

    if result:
        best_score, best_time, total_coins = result
        best_score = max(best_score, score)
        best_time = max(best_time, time)
        total_coins += coins

        cursor.execute("UPDATE players SET best_score = ?, best_time = ?, coins = ? WHERE name = ?",
                       (best_score, best_time, total_coins, name))
        conn.commit()

    conn.close()
