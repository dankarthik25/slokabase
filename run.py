
import os, sqlite3 
from slokabase import app

from flask import render_template, url_for, flash, redirect
from slokabase.forms import RegistrationForm, LoginForm, SongIndex, Song_Details



# from slokabase import SongIndex_sql, mySongs_sql
from slokabase.SqliteModel import get_create_table_query, get_insert_query, get_read_query, get_update_query, get_delete_query
from slokabase.SqliteModel import SqliteModel

# db_name = 'slokabase_10.db'
db_name = 'slokabase.db'
# db_name = 'slokabase_new.db'
db_path = os.path.join(os.getcwd(),db_name)

# SongIndex_sql = SqliteModel(db_path,'SongIndex')
# mySongs_sql = SqliteModel(db_path,'Songs' )

# song_list = SongIndex_sql.read_entry(*['song_idx', 'song_name','song_short_name'])
# mysongmy = mySongs_sql.read_entry( *['song_idx', 'slokas_no', 'sloka_eng' ,'translation'], song_idx=4) 



@app.route("/")
@app.route("/home")
def home():
    SongIndex_sql = SqliteModel(db_path,'SongIndex')
    # mySongs_sql = SqliteModel(db_path,'Songs' )

    song_list = SongIndex_sql.read_entry(*['song_idx', 'song_name','song_short_name'])
    return render_template('lib.html', song_list=song_list)

    # return render_template('sloka.html', posts=posts,)

@app.route("/lib")
def lib():
    SongIndex_sql = SqliteModel(db_path,'SongIndex')
    song_list = SongIndex_sql.read_entry(*['song_idx', 'song_name','song_short_name'])
    return render_template('lib.html', song_list=song_list,)

def get_linewise_synonym(my_sloka):
    print('get linewise synonym: my_sloka:',my_sloka)
    if my_sloka['synonyms'] !=None:
        print(my_sloka['synonyms'])
        print('before split: ',my_sloka['synonyms'].split('\n') )
        #####################################################
        synonym_list=[]
        for line in my_sloka['synonyms'].split('\n'):
            linewise_synonym_list =[]
            linewise_synonym = line.split(';')
            # linewise_synonym_list.append(line.split(';'))
            for item_string in linewise_synonym: 
                if len(item_string.split('='))==2:
                    pairs = item_string.split('=')
                    temp_dic = dict()
                    temp_dic[pairs[0].strip()] = pairs[1].strip()
                    linewise_synonym_list.append(temp_dic)
            synonym_list.append(linewise_synonym_list)
        
        print('\n ### synonym_list',synonym_list)
        #####################################################
        filtered_synonyms = ' '.join(my_sloka['synonyms'].split('\n')).split(';')
        print('# '*10)
        print('Temp synonyms : ',filtered_synonyms) 
        new_synonyms=[]
        for item in filtered_synonyms:
            if item != '':
                temp_dic = dict()
                print('item: ',item)                
                pairs = item.split('=')
                if len(pairs) == 2:
                    print('pairs:',pairs)
                    # temp_dic=dict()
                    temp_dic[pairs[0].strip()] = pairs[1].strip()
                    new_synonyms.append(temp_dic)
            # new_synonyms.append(temp_dic)
        print('# # # new_synonyms :', new_synonyms)
        my_sloka['synonyms']    = new_synonyms
    else :
        print('synonmy_list empty')
        synonym_list = None

    return synonym_list


@app.route('/lib/<int:song_id>')
def song(song_id):
    SongIndex_sql = SqliteModel(db_path,'SongIndex')
    mysong_metadata = SongIndex_sql.read_entry(song_idx=song_id)


    mySongs_sql = SqliteModel(db_path,'Songs')
    my_song = mySongs_sql.read_entry(song_idx=song_id)

    for my_sloka in my_song:
        if my_sloka['sloka_eng'] !=None: 
            my_sloka['sloka_eng']   = my_sloka['sloka_eng'].split('\n')

        # synonym_list = get_linewise_synonym(my_sloka)
        my_sloka['synonyms'] = get_linewise_synonym(my_sloka)

        if my_sloka['translation'] !=None:    
            my_sloka['translation'] = my_sloka['translation'].split('\n')
        
    return render_template('song.html', song_meta=my_song, info=mysong_metadata)




@app.route('/lib/<int:song_id>/<int:sloka_id>')
def sloka(song_id,sloka_id):
    mySongs_sql = SqliteModel(db_path,'Songs')
    my_sloka = mySongs_sql.read_entry(song_idx=song_id, slokas_no=sloka_id)

    if my_sloka[0]['sloka_eng'] !=None: 
        my_sloka[0]['sloka_eng']   = my_sloka[0]['sloka_eng'].split('\n')
    synonym_list = get_linewise_synonym(my_sloka[0])
    # if my_sloka[0]['synonyms'] !=None:
    #     print(my_sloka[0]['synonyms'])
    #     print('before split: ',my_sloka[0]['synonyms'].split('\n') )
    #     #####################################################
    #     synonym_list=[]
    #     for line in my_sloka[0]['synonyms'].split('\n'):
    #         linewise_synonym_list =[]
    #         linewise_synonym = line.split(';')
    #         # linewise_synonym_list.append(line.split(';'))
    #         for item_string in linewise_synonym: 
    #             if len(item_string.split('='))==2:
    #                 pairs = item_string.split('=')
    #                 temp_dic = dict()
    #                 temp_dic[pairs[0].strip()] = pairs[1].strip()
    #                 linewise_synonym_list.append(temp_dic)
    #         synonym_list.append(linewise_synonym_list)
        
    #     print('\n ### synonym_list',synonym_list)
    #     #####################################################
    #     filtered_synonyms = ' '.join(my_sloka[0]['synonyms'].split('\n')).split(';')
    #     print('# '*10)
    #     print('Temp synonyms : ',filtered_synonyms) 
    #     new_synonyms=[]
    #     for item in filtered_synonyms:
    #         if item != '':
    #             temp_dic = dict()
    #             print('item: ',item)                
    #             pairs = item.split('=')
    #             if len(pairs) == 2:
    #                 print('pairs:',pairs)
    #                 # temp_dic=dict()
    #                 temp_dic[pairs[0].strip()] = pairs[1].strip()
    #                 new_synonyms.append(temp_dic)
    #         # new_synonyms.append(temp_dic)
    #     print('# # # new_synonyms :', new_synonyms)
    #     my_sloka[0]['synonyms']    = new_synonyms
    # else :
    #     print('synonmy_list empty')
    #     synonym_list = None

    if my_sloka[0]['translation'] !=None:    
        my_sloka[0]['translation'] = my_sloka[0]['translation'].split('\n')
    # return my_sloka
    SongIndex_sql = SqliteModel(db_path,'SongIndex')
    song_metadata = SongIndex_sql.read_entry( *['song_name','song_short_name'] ,song_idx=song_id)
    my_sloka[0]['song_short_name'] = song_metadata[0]['song_short_name']
    my_sloka[0]['song_name'] = song_metadata[0]['song_name']

    print(my_sloka)
     
    return render_template('my_sloka.html', my_sloka_meta=my_sloka, linewise_synonym = synonym_list, song_id=song_id)


@app.route("/ppt/<int:song_id>")
def ppt(song_id):
    SongIndex_sql = SqliteModel(db_path,'SongIndex')
    mysong_metadata = SongIndex_sql.read_entry(song_idx=song_id)


    mySongs_sql = SqliteModel(db_path,'Songs')
    my_song = mySongs_sql.read_entry(song_idx=song_id)
    for my_sloka in my_song:
        if my_sloka['sloka_eng'] !=None: 
            my_sloka['sloka_eng']   = my_sloka['sloka_eng'].split('\n')
        if my_sloka['translation'] !=None:    
            my_sloka['translation'] = my_sloka['translation'].split('\n')


    return render_template('ppt.html', song_meta=my_song, info=mysong_metadata)
#     pass


if __name__ == '__main__':

    # app.run(debug=True)

    with app.app_context():
        # db.create_all()
        app.run(debug=True)

