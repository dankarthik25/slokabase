from slokabase.hindi2english import hindi2iast 
from bs4 import BeautifulSoup
import requests

def get_name_author(soup):
    container = soup.find("div", {"id": "Container"})
    song_name = container.h1.text.split('-')[0].strip() # 'Devi Aparadha Kshamapana Stotram'
    if '- composed by' in container.text: 
        song_author = container.text.split('- composed by')[1].split('\n')[0].strip() # 'Sri Adi Shankaracharya'
    else:
        song_author=None
    return song_name, song_author 

def get_sanskrit_text(soup):
    hindi_text = ''
    for verse in soup.select('span.Sanskrit'):
        for br in verse.find_all("br"):
            br.replace_with("\n")               
        hindi_text += verse.text
        hindi_text += '\n'
    
    hindi_text =hindi_text.strip()
    return hindi_text
    
def get_translation(soup):
    verse = soup.select('span.Sanskrit')[0]
    sub_containt = verse.parent#.text.split('||')
    for br in sub_containt.find_all("br"):
        br.replace_with("\n")
    output = ''
    for para in sub_containt.text.split('\n\n'):
        if 'Meaning' in para:
            # print('Meaning in para',para)
            lines = para.replace("Meaning:\n","").split('\n')
            for line in lines:
                split_list = line.split(':')
                prefix = split_list[0].strip()
                del split_list[0]
                text = '\n'.join(split_list)
                prefix_no = prefix.split('.')
                if len(prefix_no) ==2 and prefix_no[0].isnumeric() and prefix_no[1].isnumeric():
                    # print(text)
                    output +=text.strip() + '\n'
                else: 
                    # print(prefix,text) 
                    output += prefix + " " + text.strip() + '\n'
            # print()
            output +='\n'
    return output.strip()    

def scrap_word(main_word,sub_word_list):
    dict_entry= {} # dict()
    main_word = BeautifulSoup(main_word, features="html.parser").text
    words_list = main_word.split("__")
    print(words_list) # ,main_word,sub_word_list)
    dict_entry['hindi'] = words_list[1].split('(')[0].strip()
    # p_iast_word = words_list[1].split('(')[1].split(')')[0].strip()
    dict_entry['sandhi']= words_list[1].split('(')[1].split(')')[0].strip()
    # dict_entry['meaning'] = words_list[1].split('(')[1].split(')')[1].replace(':','').strip()
    dict_entry['meaning'] = words_list[1].split(':')[1].strip()
    # print(f'''{dict_entry}''')
    if isinstance(sub_word_list, list):
        print('# sub_word_list: ',sub_word_list)
        output_list = []
        for sub_word in sub_word_list:
            if len(sub_word) !=0:
                print('# Subword: ',BeautifulSoup( sub_word,features="html.parser").text)
                temp_dict = {} # dict()            
                temp_dict['hindi'] = BeautifulSoup( sub_word,features="html.parser").text.split('(')[0]
                temp_dict['sandhi']=BeautifulSoup( sub_word,features="html.parser").text.split('(')[1].split(')')[0].strip()
                temp_dict['meaning']=BeautifulSoup( sub_word,features="html.parser").text.split('(')[1].split(')')[1].replace('=','').strip()
                # print()
                # print(f'''>>>{sanskrit_word}({p_iast_word}) = {meaning_word}''')
                output_list.append(temp_dict)
        dict_entry['subwords'] = output_list
    return dict_entry

def get_query_dic(temp_dict,url):
    dicword={}
    dicword['word'] =hindi2iast(temp_dict['hindi']).strip() # word
    dicword['hindi'] =temp_dict['hindi']                     # hindi 
    dicword['sandhi'] =temp_dict['sandhi']                    # sandhi
    if 'subwords' in temp_dict.keys() : 
        dicword['subwords'] = ''
        for dict in temp_dict['subwords']:
            dicword['subwords']+=hindi2iast(dict['hindi']).strip()+'-'
        dicword['subwords'] = dicword['subwords'][:-1]
    # print(dicword) 
    # # form sl
    dicmeaning = {}
    dicmeaning['word'] = dicword['word']
    dicmeaning['source'] = url
    dicmeaning['meaning_value'] = temp_dict['meaning']
    # print(dicmeaning)
    return dicword, dicmeaning

def create_dict_entry(DictonaryMeaning_sql, DictonaryWord_sql, dicword, dicmeaning):
    if len(DictonaryWord_sql.read_entry(word=dicword['word'])) ==1:
        if len(DictonaryWord_sql.read_entry(**dicword)) ==0:
            # print(f'word:{dicword["hindi"]} already exit but what about hindi, sandi,subword')
            DictonaryWord_sql.update_entry(*['word'],**dicword)
            # (**dicword)       
    else:
        DictonaryWord_sql.create_entry(**dicword)
    if len(DictonaryMeaning_sql.read_entry(word=dicmeaning['word'],meaning_value=dicmeaning['meaning_value'])) ==1:
        pass         # already existing
    else : 
        last_idx = len(DictonaryMeaning_sql.read_entry(word=dicmeaning['word']))
        dicmeaning['meaning_idx'] = last_idx +1
        DictonaryMeaning_sql.create_entry(**dicmeaning)

def get_dic_list(line_list):
    dic_list=[]
    for idx, item in enumerate(line_list):
        if item == '' or item is None:
            continue
        if '<br/>' not in item:
            main_word = item
            sub_word =''
            dict_entry=scrap_word(main_word,sub_word)
            dic_list.append(dict_entry)
        else:
            if '<br/><br/>' in item:
                print(BeautifulSoup(item, features="html.parser").text)                
                item = item.split('<br/><br/>')[0]
                print(BeautifulSoup(item, features="html.parser").text)
            # print()
            print('# # get_dic_list: item before subword list',item)
            all_words =item.split('<br/>')
            main_word = all_words[0]
            del all_words[0]
            sub_word_list = all_words
            dict_entry=scrap_word(main_word,sub_word_list)
            dic_list.append(dict_entry)
    return dic_list

# dic_list = get_dic_list(line_list)    

def get_synonyms_byverse(mySongs_sql,sloka_no,song_idx,DictonaryWord_sql,DictonaryMeaning_sql):     
    verse_line_list = mySongs_sql.read_entry(*['sloka_eng'],song_idx=song_idx,slokas_no=sloka_no)[0]['sloka_eng'].split('\n')
    # print(verse_line_list)
    if len(verse_line_list)==4:
        verse_line_list[0] =verse_line_list[0].split('|')[0].strip()
        verse_line_list[1] =verse_line_list[1].split('|')[0].strip()
        verse_line_list[2] =verse_line_list[2].split('|')[0].strip()
        verse_line_list[3] =verse_line_list[3].split('|')[0].strip()
    elif len(verse_line_list)==2:
        verse_line_list[0] =verse_line_list[0].split('|')[0].strip()
        verse_line_list[1] =verse_line_list[1].split('|')[0].strip()        
    # print(verse_line_list)
    output = ''
    for idx,line_idx in enumerate(verse_line_list):
        # for words in line_idx.split(" "):
        for word in line_idx.split(" "): #words:
            word = word.replace('_','')  # jaṭākaṭāhasambhramabhramannilimpanirjharī_
            print(f'\t# In line {idx+1}: word={word}')
            if len(DictonaryWord_sql.read_entry(word=word)) ==0:
                error_file = open("missing_words.txt","a")
                error_entry=f"""song_idx:{song_idx}, sloka no:{sloka_no}, line no:{idx+1}, word:{word}\n""" 
                error_file.write(error_entry)
                error_file.close() 
                continue
            data = DictonaryWord_sql.read_entry(word=word)[0]
            print(f'\t  # Data in Dict.db word={data["word"]} subword={data["subwords"]}')
            if isinstance(data['subwords'],str):
                for subword in data['subwords'].split('-'):
                    output += f"""{subword}={DictonaryMeaning_sql.read_entry(word=subword)[0]['meaning_value']}; """
                    # print(f"""{subword}={DictonaryMeaning_sql.read_entry(word=subword)[0]['meaning_value']};""", end=" ")
            output += f"""{data['word']}={DictonaryMeaning_sql.read_entry(word=data['word'])[0]['meaning_value']}; """ 
            # print(f"""{data['word']}={DictonaryMeaning_sql.read_entry(word=data['word'])[0]['meaning_value']};""", end =" ")
        output= output.strip() + '\n'
    return output.strip()#)
# get_synonyms_byverse(mySongs_sql,sloka_no,meta_info['song_idx'])   
#get_synonyms_byverse(mySongs_sql,12,meta_info['song_idx'])   
