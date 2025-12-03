import sqlite3
from datetime import datetime
import os

DB_PATH = 'date_factory.db'

def get_connection():
    """Get database connection"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database with tables"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Customers table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            type TEXT NOT NULL,
            phone TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Daily prices table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS daily_prices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date DATE NOT NULL UNIQUE,
            price_per_qantar REAL NOT NULL,
            qantar_weight REAL DEFAULT 100.0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Weighbridge transactions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS weighbridge (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date DATE NOT NULL,
            customer_id INTEGER NOT NULL,
            net_weight REAL NOT NULL,
            price_per_qantar REAL NOT NULL,
            total REAL NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (customer_id) REFERENCES customers(id)
        )
    ''')
    
    # Crates table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS crates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date DATE NOT NULL,
            customer_id INTEGER NOT NULL,
            crates_out INTEGER DEFAULT 0,
            crates_returned INTEGER DEFAULT 0,
            handler TEXT,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (customer_id) REFERENCES customers(id)
        )
    ''')
    
    # Finance table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS finance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date DATE NOT NULL,
            customer_id INTEGER NOT NULL,
            transaction_type TEXT NOT NULL,
            amount_paid REAL DEFAULT 0,
            amount_received REAL DEFAULT 0,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (customer_id) REFERENCES customers(id)
        )
    ''')

    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'employee',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create indexes for better performance
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_weighbridge_customer ON weighbridge(customer_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_weighbridge_date ON weighbridge(date)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_crates_customer ON crates(customer_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_finance_customer ON finance(customer_id)')
    
    conn.commit()
    conn.close()
    print("Database initialized successfully!")

def add_sample_data():
    """Add sample data for testing"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Add sample customers
    sample_customers = [
        
    ]
    
    try:
        cursor.executemany('INSERT OR IGNORE INTO customers (name, type, phone) VALUES (?, ?, ?)', 
                          sample_customers)
        
        # Add sample price
        cursor.execute('INSERT OR IGNORE INTO daily_prices (date, price_per_qantar) VALUES (?, ?)',
                      (datetime.now().strftime('%Y-%m-%d'), 150.0))
        
        # Add default admin user (password: admin123)
        # We store it as plain text for initial setup to ensure it works on all devices.
        # The app supports upgrading to hashed passwords later or handling plain text.
        admin_pass = 'admin123'

        cursor.execute('INSERT OR IGNORE INTO users (username, password, role) VALUES (?, ?, ?)',
                      ('admin', admin_pass, 'admin'))

        conn.commit()
        print("Sample data added successfully!")
    except Exception as e:
        print(f"Error adding sample data: {e}")
    finally:
        conn.close()

if __name__ == '__main__':
    init_db()
    add_sample_data()
