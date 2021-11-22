import sqlite3
import os
import time
import chardet

# Create database for storing information about file encodings
conn = sqlite3.connect('data/encoding.sqlite')
cur = conn.cursor()

# Create tables for data
cur.executescript('''
CREATE TABLE IF NOT EXISTS Files (
    name TEXT UNIQUE,
    encoding_id INTEGER,
    times_read INTEGER
);

CREATE TABLE IF NOT EXISTS Encodings (
    encoding_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    encoding TEXT UNIQUE
)
''')

# Writing information to database
for paths, dirs, files in os.walk('raw_data'):
    i = 0
    for file in files:
        if file.startswith('.'):
            continue
        filePath = os.path.join(paths, file)
        with open(filePath) as openFile:
            encoding = openFile.encoding
        cur.execute('SELECT name FROM Files WHERE name = ?', (file,))
        check = cur.fetchone()
        if check:
            # print('File info already stored')
            continue
        else:
            cur.execute(
                'INSERT OR IGNORE INTO Encodings (encoding) VALUES (?)', (encoding,))
            cur.execute(
                'SELECT encoding_id FROM Encodings WHERE encoding = ?', (encoding,))
            encodingId = cur.fetchone()[0]

            cur.execute('''INSERT OR IGNORE INTO Files
            (name, encoding_id, times_read) VALUES (?, ?, ?)''', (file, encodingId, 0))
        i = i + 1
        if i == 50000:
            conn.commit()
            print('commit')
            print('sleep for 5 seconds')
            time.sleep(5)
            i = 0
conn.commit()
conn.close()



# Testing