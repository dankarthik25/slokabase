import os, sqlite3 
db_name = 'slokabase.db'
db_path = os.path.join(os.getcwd(),db_name)

SongIndex_sql = SqliteModel(db_path,'SongIndex')
mySongs_sql = SqliteModel(db_path,'Songs')

db_name = 'dictionary.db'
db_path = os.path.join(os.getcwd(),db_name)
DictonaryWord_sql = SqliteModel(db_path,'DictWord')
DictonaryMeaning_sql = SqliteModel(db_path,'DictMeaning')

DictonaryWord_sql.create_table(word ='VARCHAR(300) NOT NULL UNIQUE',
                    phonetics = 'VARCHAR(300)',
                    word_idx='INTEGER AUTO INCREMENT', 
                    PRIMARY= 'KEY (word)')


DictonaryMeaning_sql.create_table(word='VARCHAR(300)', 
                    meaning_idx='INTEGER NOT NULL', 
                    meaning_value='TEXT NOT NULL',
                    meaning_type= 'VARCHAR(100)', 
                    reference='TEXT',
                    example='TEXT', 
                    synonyms= 'TEXT',      
                    source= 'TEXT',  
                    FOREIGN = 'KEY (word) REFERENCES DictonaryWord_sql(word)',
                    PRIMARY= 'KEY (word, meaning_value)')

#ALTER TABLE DictMeaning ADD reference_green VARCHAR(30000);

# grammer, singular/pular, gender,part of speech, 1st, 2nd, 3rd person
# like hypter link bg1.2,sb 1.2.4, song_id.verse_no
# similar synonyms
# hyper links
