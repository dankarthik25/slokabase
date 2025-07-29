#!/usr/bin/env python
# coding: utf-8

# In[1]:


from slokabase.WebScrapGreen import *
import os
from slokabase.SqliteModel import get_create_table_query, get_insert_query, get_read_query, get_update_query, get_delete_query
from slokabase.SqliteModel import SqliteModel
from slokabase.hindi2english import hindi2iast 
from bs4 import BeautifulSoup
import requests


# In[2]:


db_name = 'dictionary.db'
db_path = os.path.join(os.getcwd(),db_name)
DictonaryWord_sql = SqliteModel(db_path,'DictWord')
DictonaryMeaning_sql = SqliteModel(db_path,'DictMeaning')

db_name = 'slokabase.db'
db_path = os.path.join(os.getcwd(),db_name)
SongIndex_sql = SqliteModel(db_path,'SongIndex')
mySongs_sql = SqliteModel(db_path,'Songs')


# In[3]:


# url = 'https://greenmesg.org/stotras/durga/devi_aparadha_kshamapana_stotram.php'
# url = 'https://greenmesg.org/stotras/annapoorna/annapoorna_stotram.php'
# url = 'https://greenmesg.org/stotras/vishnu/venkatesa_suprabhatam.php'
# url ='https://greenmesg.org/stotras/shiva/shiva_tandava_stotram.php'
# url = 'https://greenmesg.org/stotras/rama/nama_ramayana.php'
url = 'https://greenmesg.org/stotras/shiva/dakshinamurthy_stotram.php'

# ##### 1st Step: `DONE` Scrapp song form website

# In[4]:


source = requests.get(url).text
soup = BeautifulSoup(source, features="html.parser")
song_name, song_author = get_name_author(soup)
hindi_text       = get_sanskrit_text(soup)
iast_text = hindi2iast(hindi_text)
translation_text = get_translation(soup)


# In[5]:


# print(translation_text)
# print(iast_text)
# print(hindi_text)
print(len(hindi_text.split('\n\n')), len( translation_text.split('\n\n') )  )
if len(hindi_text.split('\n\n'))!=len( translation_text.split('\n\n') ) :
    import sys
    sys.exit("Error message")
    # break


# ##### 2st Step: `DONE` create new song[with out synonyms] in slokabase.db

# In[6]:


# SongIndex_sql.create_entry(**song_info)
song_info = {}
song_info['song_name'] = song_name# +'1' # 'My Dasavatara Stotram'
song_info['song_short_name'] = song_info['song_name'] .replace(" ","") # 'MyDasaVatStot'
song_info['sloka_statues'] = 1
song_info['division_no'] = 0
song_info['total_slokas'] = len(hindi_text.split('\n\n'))
# song_info['groups']
# song_info['devotion_god']
if song_author is not None:
    song_info['author']= song_author 
# song_info['describtion']=  
song_info['other_links '] = url
print(song_info)    


# In[7]:


if len(SongIndex_sql.read_entry(**song_info)) ==0:
    SongIndex_sql.create_entry(**song_info)
    print('Created new song entry in songindex:')
    
song_idx = SongIndex_sql.read_entry( *['song_idx'], **song_info)[0]['song_idx'] # >>> 5
print(SongIndex_sql.read_entry( *['song_idx'], **song_info))


# In[8]:


song = dict()
song['sloka_eng'] = iast_text
song['sloka_hindi'] = hindi_text
song['translation'] = translation_text
# print(song)


# In[9]:


mysong = dict()
# mySongs_sql = SqliteModel(db_path,'Songs')
mysong ['song_idx'] = SongIndex_sql.read_entry(*['song_idx'], **song_info)[0]['song_idx']

list_sloka = song['sloka_eng'].split('\n\n')
for idx, sloka in enumerate(list_sloka):
    mysong['slokas_no']   = idx+1
    mysong['sloka_eng']   = sloka.strip()
    print(f"[sloka_eng] new entry  in song idx :{mysong['song_idx']} and verse={idx+1}")    
    mySongs_sql.create_entry(**mysong)
del mysong['sloka_eng']

list_sloka = song['sloka_hindi'].split('\n\n')
for idx, sloka in enumerate(list_sloka):
    # print(idx)
    mysong['slokas_no']   = idx+1
    mysong['sloka_hindi']   = sloka.strip()
    print(f"[sloka_hindi] new entry  in song idx :{mysong['song_idx']} and verse={idx+1}")    
    mySongs_sql.update_entry( *['song_idx','slokas_no']  , **mysong)
del mysong['sloka_hindi']

list_sloka = song['translation'].split('\n\n')    
for idx, sloka in enumerate(list_sloka):
    # print(idx)
    mysong['slokas_no']   = idx+1
    mysong['translation']   = sloka.strip()
    print(f"[translation] new entry  in song idx :{mysong['song_idx']} and verse={idx+1}")        
    mySongs_sql.update_entry( *['song_idx','slokas_no']  , **mysong)
del mysong['translation']


# ##### 3nd Step: `TODO` Create new word(key,meaning) in dictionary.db

# In[10]:


x =requests.request('GET', url.replace('stotras','dictionary/stotras').replace('php','txt') )
line_list = x.text.split('\r\n')
for dict_entry in get_dic_list(line_list):
    dicword, dicmeaning = get_query_dic(dict_entry,url)    
    create_dict_entry(DictonaryMeaning_sql, DictonaryWord_sql, dicword, dicmeaning)
    print('# mainword:',dicword, dicmeaning ) 
    if 'subwords' in dict_entry.keys() :     
        for dict_subword in dict_entry['subwords']:
            dicword, dicmeaning = get_query_dic(dict_subword,url)    
            create_dict_entry(DictonaryMeaning_sql, DictonaryWord_sql, dicword, dicmeaning)
            print('\t# subword:',dicword, dicmeaning)
            # print(dicword, dicmeaning ) 


# ##### 4th Step: `TODO` Update synonyms col in song table in slokabase.db

# In[13]:


# def get_synonyms_byverse1(mySongs_sql,sloka_no,song_idx,DictonaryWord_sql,DictonaryMeaning_sql):  
#     verse_line_list = mySongs_sql.read_entry(*['sloka_eng'],song_idx=song_idx,slokas_no=sloka_no)[0]['sloka_eng'].split('\n')
#     # print(verse_line_list)
#     if len(verse_line_list)==4:
#         verse_line_list[0] =verse_line_list[0].split('|')[0].strip()
#         verse_line_list[1] =verse_line_list[1].split('|')[0].strip()
#         verse_line_list[2] =verse_line_list[2].split('|')[0].strip()
#         verse_line_list[3] =verse_line_list[3].split('|')[0].strip()
#     elif len(verse_line_list)==2:
#         verse_line_list[0] =verse_line_list[0].split('|')[0].strip()
#         verse_line_list[1] =verse_line_list[1].split('|')[0].strip()        
#     # print(verse_line_list)
#     output = ''
#     for idx,line_idx in enumerate(verse_line_list):
#         # for words in line_idx.split(" "):
#         for word in line_idx.split(" "): #words:
#             # word = words[4]
#             print(f'\t# In line {idx+1}: word={word}')
#             data = DictonaryWord_sql.read_entry(word=word)[0]
#             print(f'\t  # Data in Dict.db word={data["word"]} subword={data["subwords"]}')
#             if isinstance(data['subwords'],str):
#                 for subword in data['subwords'].split('-'):
#                     output += f"""{subword}={DictonaryMeaning_sql.read_entry(word=subword)[0]['meaning_value']}; """
#                     # print(f"""{subword}={DictonaryMeaning_sql.read_entry(word=subword)[0]['meaning_value']};""", end=" ")
#             output += f"""{data['word']}={DictonaryMeaning_sql.read_entry(word=data['word'])[0]['meaning_value']}; """ 
#             # print(f"""{data['word']}={DictonaryMeaning_sql.read_entry(word=data['word'])[0]['meaning_value']};""", end =" ")
#         output= output.strip() + '\n'
#     return output.strip()#)
# # get_synonyms_byverse(mySongs_sql,sloka_no,meta_info['song_idx'])   
# #get_synonyms_byverse(mySongs_sql,12,meta_info['song_idx'])   


# In[12]:


meta_info = SongIndex_sql.read_entry(**song_info)[0]#['song_idx']
print(meta_info)
total_no_verse = meta_info['total_slokas']
for sloka_no in range(1,total_no_verse+1):
    # sloka_no = 1 # 
    print('# Sloka No:',sloka_no)
    if mySongs_sql.read_entry(song_idx=meta_info['song_idx'],slokas_no=sloka_no)[0]['synonyms'] is  None:
        synonyms_by_verse = get_synonyms_byverse(mySongs_sql,sloka_no,meta_info['song_idx'],DictonaryWord_sql,DictonaryMeaning_sql)
        mySongs_sql.update_entry( *['song_idx','slokas_no'],synonyms=synonyms_by_verse, song_idx=meta_info['song_idx'], slokas_no=sloka_no)


# In[11]:


# mysong_index =77
# mySongs_sql.delete_entry(song_idx=mysong_index) # delete all verse or sloka
# SongIndex_sql.delete_entry(song_idx=mysong_index) # delete in index table


# In[ ]: