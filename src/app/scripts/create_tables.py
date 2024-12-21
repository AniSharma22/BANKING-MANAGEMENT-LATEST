import sqlite3
import src.app.config.config as config

# Open connection and enable foreign key support explicitly for SQLite
conn = sqlite3.connect(config.DB_ADDR)
conn.execute("PRAGMA foreign_keys = ON;")  # Enabling foreign key support for SQLite

with conn:
    # Creating the tables one by one
    conn.execute('''
        CREATE TABLE IF NOT EXISTS banks (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL
        );
    ''')

    conn.execute('''
        CREATE TABLE IF NOT EXISTS branches (
            id TEXT PRIMARY KEY,
            bank_id TEXT NOT NULL,
            name TEXT NOT NULL,
            address TEXT NOT NULL,
            FOREIGN KEY (bank_id) REFERENCES banks(id) ON DELETE CASCADE
        );
    ''')

    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            phone_no TEXT NOT NULL,
            address TEXT NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('user', 'admin'))
        );
    ''')

    conn.execute('''
        CREATE TABLE IF NOT EXISTS accounts (
            id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            branch_id TEXT NOT NULL,
            bank_id TEXT NOT NULL,
            balance INTEGER NOT NULL DEFAULT 0 CHECK(balance >= 0),
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (branch_id) REFERENCES branches(id) ON DELETE CASCADE,
            FOREIGN KEY (bank_id) REFERENCES banks(id) ON DELETE CASCADE
        );
    ''')

    conn.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id TEXT PRIMARY KEY,
            amount INTEGER NOT NULL,
            transaction_type TEXT NOT NULL CHECK(transaction_type IN ('deposit', 'withdraw', 'transfer')),
            sender_acc_id TEXT,
            receiver_acc_id TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (sender_acc_id) REFERENCES accounts(id) ON DELETE CASCADE,
            FOREIGN KEY (receiver_acc_id) REFERENCES accounts(id) ON DELETE CASCADE
        );
    ''')
