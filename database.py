import sqlite3

DB_NAME = "bingo.db"


def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    cur = conn.cursor()

    # Users
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_id INTEGER UNIQUE,
        username TEXT,
        balance REAL DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Deposits
    cur.execute("""
    CREATE TABLE IF NOT EXISTS deposits(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        amount REAL,
        screenshot TEXT,
        status TEXT DEFAULT 'pending',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Games
    cur.execute("""
    CREATE TABLE IF NOT EXISTS games(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        status TEXT DEFAULT 'waiting',
        winner INTEGER,
        prize REAL DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Bingo Cards
    cur.execute("""
    CREATE TABLE IF NOT EXISTS cards(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        game_id INTEGER,
        numbers TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()


# ---------------- USERS ----------------

def create_user(telegram_id, username):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
    INSERT OR IGNORE INTO users
    (telegram_id, username)
    VALUES (?, ?)
    """, (telegram_id, username))

    conn.commit()
    conn.close()


def get_user(telegram_id):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
    SELECT * FROM users
    WHERE telegram_id=?
    """, (telegram_id,))

    user = cur.fetchone()

    conn.close()

    return user


# ---------------- BALANCE ----------------

def add_balance(telegram_id, amount):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
    UPDATE users
    SET balance = balance + ?
    WHERE telegram_id=?
    """, (amount, telegram_id))

    conn.commit()
    conn.close()


def deduct_balance(telegram_id, amount):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
    UPDATE users
    SET balance = balance - ?
    WHERE telegram_id=?
    """, (amount, telegram_id))

    conn.commit()
    conn.close()


# ---------------- DEPOSIT ----------------

def create_deposit(user_id, amount, screenshot):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO deposits
    (user_id, amount, screenshot)
    VALUES (?, ?, ?)
    """, (user_id, amount, screenshot))

    conn.commit()
    conn.close()


def approve_deposit(deposit_id):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
    UPDATE deposits
    SET status='approved'
    WHERE id=?
    """, (deposit_id,))

    conn.commit()
    conn.close()


# ---------------- GAME ----------------

def create_game():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO games(status)
    VALUES('waiting')
    """)

    game_id = cur.lastrowid

    conn.commit()
    conn.close()

    return game_id
# ---------------- CARD ----------------

def save_card(user_id, game_id, numbers):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO cards (user_id, game_id, numbers)
        VALUES (?, ?, ?)
    """, (user_id, game_id, numbers))

    conn.commit()
    conn.close()


# ---------------- DEPOSIT ----------------

def save_deposit(user_id, amount, screenshot):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO deposits (user_id, amount, screenshot)
        VALUES (?, ?, ?)
    """, (user_id, amount, screenshot))

    conn.commit()
    conn.close()
def get_current_game():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
    SELECT * FROM games
    WHERE status='waiting'
    ORDER BY id DESC
    LIMIT 1
    """)

    game = cur.fetchone()

    conn.close()

    return game
    def get_player_card_count(telegram_id, game_id):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
    SELECT COUNT(*)
    FROM cards
    WHERE user_id=? AND game_id=?
    """, (telegram_id, game_id))

    count = cur.fetchone()[0]

    conn.close()

    return count
    def add_prize_pool(game_id, amount):

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
    UPDATE games
    SET prize = prize + ?
    WHERE id=?
    """, (amount, game_id))

    conn.commit()
    conn.close()
    # ---------------- CURRENT GAME ----------------

def get_current_game():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT *
        FROM games
        WHERE status='waiting'
        ORDER BY id DESC
        LIMIT 1
    """)

    game = cur.fetchone()

    conn.close()

    return game


# ---------------- PLAYER CARD COUNT ----------------

def get_player_card_count(user_id, game_id):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT COUNT(*) AS total
        FROM cards
        WHERE user_id=?
        AND game_id=?
    """, (user_id, game_id))

    total = cur.fetchone()["total"]

    conn.close()

    return total


# ---------------- PRIZE POOL ----------------

def add_prize_pool(game_id, amount):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        UPDATE games
        SET prize = prize + ?
        WHERE id=?
    """, (amount, game_id))

    conn.commit()
    conn.close()
