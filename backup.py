from slokabase.SqliteModel import get_create_table_query, get_insert_query, get_read_query, get_update_query, get_delete_query
from slokabase.SqliteModel import SqliteModel
import os, sqlite3 
import json

def write_song(file_path, song_type, mySongs_sql, mysong_idx):
    start_sloka_no=0
    buffer = []
    for line in mySongs_sql.read_entry(*[song_type,'slokas_no'],song_idx=mysong_idx):
        if line[song_type] != None:
            buffer.append(line[song_type])
            if start_sloka_no != line['slokas_no']:
                buffer.append('\n\n')
            start_sloka_no = line['slokas_no']

    if len(buffer) !=0:
            del buffer[-1]
    # print(buffer)
    # print(''.join(buffer))
    with open(file_path, 'w') as wf:
        wf.write(''.join(buffer))

####################################################
db_name = './slokabase.db'
db_path = os.path.join(os.getcwd(),db_name)

SongIndex_sql = SqliteModel(db_path,'SongIndex')
mySongs_sql = SqliteModel(db_path,'Songs')



backup_dir = 'SlokaBackUp'
if not os.path.exists(backup_dir):
   os.makedirs(backup_dir)

# songIdx_info
index_list = []
for idx_dic in SongIndex_sql.read_entry(*['song_idx']):
    # print(idx_dic['song_idx'])
    index_list.append(idx_dic['song_idx'])
index_list.sort()

for song_idx in index_list:
# song_idx = 1
    songIdx_info = SongIndex_sql.read_entry(song_idx=song_idx)[0]
    song_name = songIdx_info['song_name'].replace(" ","")
    song_type = ['sloka_eng', 'synonyms','translation']

    for s_type in song_type:
        file_name = f'{song_idx:04}-{song_name}-{s_type}.txt'
        file_path = os.path.join(backup_dir,file_name)
        write_song(file_path, s_type, mySongs_sql,song_idx)
        print(file_path)

    file_name = f'{song_idx:04}-{song_name}-info.json'
    file_path = os.path.join(backup_dir,file_name)
    with open(file_path, "w") as wjson:
        json.dump(songIdx_info, wjson)
    print(file_path)



import pandas as pd 
data = SongIndex_sql.read_entry()
df = pd.DataFrame(data)
file_path = os.path.join(backup_dir,'index.csv')
df.to_csv(file_path,index=False)





