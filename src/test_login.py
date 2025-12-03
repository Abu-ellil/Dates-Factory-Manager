import sqlite3
from werkzeug.security import check_password_hash

conn = sqlite3.connect('date_factory.db')
user = conn.execute('SELECT * FROM users WHERE username = ?', ('admin',)).fetchone()

print(f'Username: {user[1]}')
print(f'Password in DB: {user[2]}')
print(f'Password starts with scrypt: {user[2].startswith("scrypt:")}')

test_pass = 'admin123'
if user[2].startswith('scrypt:'):
    print(f'Hash check result: {check_password_hash(user[2], test_pass)}')
else:
    print(f'Plain text check result: {user[2] == test_pass}')

conn.close()
