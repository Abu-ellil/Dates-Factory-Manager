import sqlite3
import os

db_files = [
    r'c:\Users\MAS\Desktop\QQQ\bin\date_factory.db',
    r'c:\Users\MAS\Desktop\QQQ\date_factory.db',
    r'c:\Users\MAS\Desktop\QQQ\src\date_factory.db'
]

for db_path in db_files:
    if os.path.exists(db_path):
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Check if admin user exists
            user = cursor.execute('SELECT * FROM users WHERE username = ?', ('admin',)).fetchone()
            
            if user:
                # Update password to plain text
                cursor.execute('UPDATE users SET password = ? WHERE username = ?', ('admin123', 'admin'))
                conn.commit()
                print(f'✅ Updated password in: {db_path}')
            else:
                # Create admin user
                cursor.execute('INSERT INTO users (username, password, role) VALUES (?, ?, ?)',
                             ('admin', 'admin123', 'admin'))
                conn.commit()
                print(f'✅ Created admin user in: {db_path}')
            
            conn.close()
        except Exception as e:
            print(f'❌ Error with {db_path}: {e}')
    else:
        print(f'⚠️  File not found: {db_path}')

print('\n✅ All database files updated!')
