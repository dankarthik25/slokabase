import os, sqlite3 

db_name = 'slokabase.db'
db_path = os.path.join(os.getcwd(),db_name)

SongIndex_sql = SqliteModel(db_path,'SongIndex')
mySongs_sql = SqliteModel(db_path,'Songs')

# Create Table if Not Created 

SongIndex_sql.create_table(
                    song_idx='INTEGER PRIMARY KEY' , 
                    song_name='VARCHAR(100) NOT NULL UNIQUE', 
                    song_short_name='VARCHAR(100) NOT NULL UNIQUE', 
                    sloka_statues='BOOLEAN NOT NULL CHECK (sloka_statues IN (0, 1))',
                    division='VARCHAR(100)',
                    division_no='INTEGER',
                    total_slokas='INTEGER',
                    groups='VARCHAR(100)',
                    devotion_god='VARCHAR(100)',
                    author='VARCHAR(100)',
                    describtion='TEXT',
                    other_links='TEXT'
                    )


mySongs_sql.create_table(song_idx='INTEGER', 
                    slokas_no='INTEGER NOT NULL', 
                    sloka_hindi= 'TEXT',
                    sloka_eng= 'TEXT',
                    synonyms= 'TEXT',
                    translation= 'TEXT',
                    purpot= 'TEXT',
                    FOREIGN = 'KEY (song_idx) REFERENCES SongIndex(song_idx)',
                    PRIMARY= 'KEY (song_idx, slokas_no)')
