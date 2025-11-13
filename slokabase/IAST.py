import sqlite3
import sys
import os

class IAST():
    vowel_plist=[['r̥̄', 'l̥̄'], 
                 ['r̥', 'au', 'ai', 'ụ̄ ', 'ạ̄ ', 'oṁ', 'm̐', 'aḥ', 'l̥'], 
                 ['a', 'ā', 'ạ', 'ụ', 'æ', 'ǣ', 'i', 'ī', 'u', 'ū', 'e', 'ē', 'ê', 'ê',
                  'o', 'ǒ', 'ō', 'ô', 'ʻ', 'ḥ', 'ḫ', 'ẖ', 'ṁ', 'ṃ']]
    
    consonant_list = [['n̆g', 'n̆j', 'n̆ḍ', 'n̆d', 'm̆b', 'k͟h'], 
                       ['kh', 'g̈', 'gh', 'ch', 'ĉh', 'jh', 'ṭh', 'ḍh', 'dh', 'd̤', 
                        'ṛh', 'th', 'ph', 'bh', 'b̤', 'ṟ̄', 'y̌', 'r̆', 'l̤', '||'], 
                       ['ḵ', 'k', 'g', 'ṅ', 'c', 'ĉ', 'j', 'ǰ', 'ĵ', 'ñ', 'ṭ', 'ḍ', 'ḍ', 
                        'ṛ', 'ṇ', 't', 'd', 'n', 'p', 'b', 'm', 'ṟ', 'ṯ', 'ḏ', 'ṉ',
                        'ḻ', 'y', 'ẏ', 'r', 'l', 'ḷ', 'v', 'ś', 'ṣ', 's', 'h', 'q', 'ġ', 
                        'z', 'z', 'ž', 'ž', 'ž', 'f', 's̱', 's̤', 'h̤', 't̤', 'w',
                        'ẕ', 'ż', 'ẓ', 'ẏ', 'ṟ', 
                        '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '|']]
    
    # Phonetic Search Static Variables
    zero_vowels={ '':['a', "ā", "â","i", "ī","u", "ū",chr(805),chr(803),
                      "l̥", "l̥̄","e", "ē", "ê","o", "ō", "ô",
                      "ṁ", "m̐", "ṃ", "ṃ","n̆", "n̆", "n̆","ḥ" , "ḫ", "ẖ", "ḥ"],
                  'r': ["r̥", "r̥̄"]
                } # replacing with r is not working for 'r̥' so we replace with chr(805) above
    truncated_vowels = { '':[chr(805), chr(803), chr(772),chr(784),chr(774)],
                        'a':["ā", "â"], 
                        'i':["i", "ī"], 
                        'u':["u", "ū"], 
                        'r':["r̥", "r̥̄"],
                        'l':["l̥", "l̥̄"],
                        "e":["e", "ē", "ê"],
                                # "ai", 
                        "o": ["o", "ō", "ô"], 
                                                # "au",
                        'm' :["ṁ", "m̐", "ṃ", "ṃ"], 
                        'n': ["n̆", "n̆", "n̆"], 
                        'h' :["ḥ" , "ḫ", "ẖ", "ḥ"],
                        }
    basic_truncated_consonat = {
                        'k' : ['ḵ', 'k', 'kh','k͟ha'],
                        'g' :['g','g̈','gh','ġ'],
                        'n' : ['ṅ','n̆','ñ','ṇ','ṉ'],
                        'c' : ['c', 'ĉ','ch','ĉh'],
                        'j' : ['j','ǰ', 'ĵ', 'jh'],
                        't': ['ṭ','ṭa','t','th','ṯ','t̤'],
                        'd' : ['ḍ', 'd̤','ḍ','ḍh','d','dh','ḏ'],
                        'p' : ['p', 'ph'],
                        'b' : [ 'b', 'b̤', 'bh'],
                        'm' : ['m̆' ],
                        'r' : ['ṟ', 'r̆'],
                        'l' :['ḻ', 'ḷ', 'l̤'],
                        'y' : ['y', 'ẏ', 'y̌'],
                        's': ['ś', 'ṣ', 's','s̱', 's̤','sh' ],
                        "z": ["z","ž","ž","ž",'ẕ','ẕ','ẓ','ż'],
                        'h' : ['h','h̤']
                        }
    
    
    def __init__(self,db_path=None,table_name_alpha='IndianAlphabet',table_name_barakadi='Barakhadi',table_name_inv_alpha='InvAlpha',table_name_inv_bara='InvBara' ):
        if db_path is None:
            dir_path = os.path.dirname(__file__)
#            dir_path = os.getcwd()
            self.db_path=os.path.join(dir_path,'iast-token.db')
#            self.db_path=os.path.join(dir_path,'iastv3.db')
#            self.db_connect = sqlite3.connect(os.path.join(dir_path,'iast-token.db'))
        else:
            self.db_path=db_path

#        print('db_path: ',self.db_path,type(self.db_path))

        self.db_connect = sqlite3.connect(self.db_path)
        self.alphabet = table_name_alpha
        self.barakhadi = table_name_barakadi
        self.inv_alphabet = table_name_inv_alpha
        self.inv_barakhadi = table_name_inv_bara
        self.halant_list = self.get_halant_list() #  ['्', '্', '્', '್', '്', '୍', '్']
# phonetic search algo inicialization
    def set_query(self,query):
        db_cursor = self.db_connect.cursor()
        try :
            db_cursor.execute(query)    
        except sqlite3.Error as e:
            print('SQLite error: %s' % (' '.join(e.args)))
            print("Exception class is: ", e.__class__)
            print('SQLite traceback: ')
            exc_type, exc_value, exc_tb = sys.exc_info()
            # data = []
        
        finally:
            self.db_connect.commit()
            # auto_increment and delete on cascade https://stackoverflow.com/questions/29037793/sqlite-integrityerror-unique-constraint-failed
            sefl.db_cursor.close()
            # db_cursor.close()
            # print('Read Query!')
        # return data
    
    def get_query(self,query): # all query which will give or get the data or query which will return some value
        db_cursor = self.db_connect.cursor()
        try :
            db_cursor.execute(query)    
            columns = [column[0] for column in db_cursor.description]
            data = [dict(zip(columns, row)) for row in db_cursor.fetchall()]
            # self.db_connect.close()
        except sqlite3.Error as e:
            print('SQLite error: %s' % (' '.join(e.args)))
            print("Exception class is: ", e.__class__)
            print('SQLite traceback: ')
            exc_type, exc_value, exc_tb = sys.exc_info()
            data = []
        
        finally:
            # db_connect.commit()
            # auto_increment and delete on cascade https://stackoverflow.com/questions/29037793/sqlite-integrityerror-unique-constraint-failed
            db_cursor.close()
            # db_cursor.close()
            # print('Read Query!')
        return data
    
    def get_iast_idx_query(letter,talbe_name): # query: given indic letter will return iast mapped value 
        query =f"""SELECT * FROM {talbe_name} WHERE Devanagari == '{letter}' OR Bengali–Assamese == '{letter}' OR Gujarati == '{letter}' OR Kannada == '{letter}' OR Malayalam == '{letter}' OR Odia == '{letter}' OR Tamil == '{letter}' OR Telugu == '{letter}';"""

        return query 

    def get_halant_list (self):
        letter = 'ŭ'
        query = f"SELECT * FROM {self.barakhadi} WHERE IAST='{letter}'" 
        data =self.get_query(query)
        # print(data)
        del data[0]['IAST']
        halant_list = []
        for value in data[0].values():
            if value is not None and value not in halant_list:
                halant_list.append(value)
        # print(halant_list)
        return halant_list

    # word = 'ధృత్రాష్ట్ర ఉవాచ'
    def to_iast(self,word): # arg can be word, sentance, line, para, whole doc
        output_token = ''
        for letter in word: # word
            query = IAST.get_iast_idx_query(letter,self.alphabet)    
            alpha_token =self.get_query(query)
            
            query = IAST.get_iast_idx_query(letter,self.barakhadi)    
            barakhadi_token =self.get_query(query)
            
            if len(alpha_token) !=0:
                output_token += alpha_token[0]['IAST']
                # print(alpha_token[0]['IAST'],end='')
            elif letter in  self.halant_list and output_token[-1] in "a": 
                        # >> 'क्' = 'क ' +'्'   # >>> ka + halant = k
                output_token = output_token[:-1]
            elif len(barakhadi_token) !=0 and output_token[-1] in "a":
                        #  'कि'='क ' + 'ि' = ka + i => ki
                output_token = output_token[:-1]+ barakhadi_token[0]['IAST']
            elif len(barakhadi_token) !=0 :
                        #   ' किं ' = ='क ' + 'ि' + 'ं'  = ka + i + aṁ = kiṁ
                output_token += barakhadi_token[0]['IAST'].replace("a",'')
            elif len(barakhadi_token) ==0  and len(alpha_token) ==0 and ord(letter)==8205: # cleaing data
                pass
            else:
                # print(f"""NOT Present in alpha and barakadi{letter}=={ord(letter)} """)
                output_token += letter
            # print(out)
            # print(f'{letter}\t| {output_token}')
        # print(f'{word}\t| {output_token}')
        return output_token
    # iast.to_iast( word)

    def debug_letterbyletter(self,text):
    # text =' ധർമക്ഷേത്രേ കുരുക്ഷേത്രേ സമവേതാ യുയുത്സവഃ ।' #	| dhaർmakṣētrē kurukṣētrē samavētā yuyutsavaḥ |  
        for letter in text: 
            query = IAST.get_iast_idx_query(letter,self.alphabet)    
            alpha_token =self.get_query(query)
            
            query = IAST.get_iast_idx_query(letter,self.barakhadi)    
            barakhadi_token =self.get_query(query)
            
            output_token=''
            if len(alpha_token) !=0:
                output_token += alpha_token[0]['IAST']
                # print(alpha_token[0]['IAST'],end='')
            elif len(barakhadi_token) !=0 :
                output_token = output_token[:-1]+ barakhadi_token[0]['IAST']
            else:
                output_token = letter
                
            output = f'letter= {letter} \t| ascii(letter) ={ord(letter[0])}\t| iast = {output_token}' #  | ascii(iast)={ord(iast_letter)}'
            print(output)

# Methods for phonetic search
    # Replace many to one
    
    def replace_m2o(text, source=None, dest=None): # 
        if isinstance(source, list):
            for source_letter in source:
                text = text.replace(source_letter,dest)
        elif isinstance(source, str):
            text = text.replace(source,dest)
        # print(text)
        return text
        
    # Replace many to many
    def replace_m2m(output_data,info_dict):
        for dest in info_dict.keys():
            source = info_dict[dest]
            output_data = IAST.replace_m2o(output_data, source=source, dest=dest)
        return output_data

    # Basic Stemming
    def basic_hash(iast_text): # if text is in hin,kan,tel,mal,guj,..etc need to convert to iast 
        basic_stem_dict = IAST.zero_vowels
        basic_stem_dict.update(IAST.basic_truncated_consonat)
        output =IAST.replace_m2m(iast_text,basic_stem_dict)
        return output
        
    # Normal Stemming
    def normal_hash(iast_text):
        normal_stem_dict = IAST.truncated_vowels
        normal_stem_dict.update(IAST.basic_truncated_consonat)
        output = IAST.replace_m2m(iast_text,normal_stem_dict)
        return output
    
    def get_indic_symbol_query(iast_letter,language,table_name): # query given indic letter will return iast mapped value 
        # query =f"""
        # SELECT type {language} FROM {table_name} 
        # WHERE IAST LIKE '{iast_letter}%';
        # """
        query =f"""SELECT type, IAST, {language}  FROM {table_name} 
        WHERE IAST LIKE '{iast_letter}%';
        """
 # 'type': 'consonants',
 #  'IAST': 'gha',
 #  'Devanagari': 'घ',
 #  'Bengali–Assamese': 'ঘ',
 #  'Gujarati': 'ઘ',
 #  'Gurmukhi': 'ਘ',
        # print(query.replace('\n','').replace("  ","")) 
    # SELECT * FROM IndianAlphabet WHERE Devanagari == 'ध' OR Bengali–Assamese == 'ध' OR Gujarati == 'ध' OR Kannada == 'ध' OR Malayalam == 'ध' OR Odia == 'ध' OR Tamil == 'ध' OR Telugu == 'ध'    
        return query 
        
# iast to indic language(any lang) 
    
    def lex_iast(keyword, word):
        tokens=[]
        # print(keyword,word)
        slic_pstart = 0 # previous start point
        # slic_pstart = 0 # previous start point
        # slic/_pstart = 0 # previous start point
        
        len_word = len(word)
        slic3_flag = False
        slic2_flag = False
        slic1_flag = False
        
        for idx, letter in enumerate(word):
            slic3 = word[idx:idx+3]
            if slic3 in keyword[0]:
                slic3_flag=True
            else:
                slic3_flag=False
            slic2 = word[idx:idx+2]            
            if slic2 in keyword[1]:
                slic2_flag=True
            else:
                slic2_flag=False        
            slic1 = word[idx:idx+1]        
            if slic1 in keyword[2]:
                slic1_flag=True
            else:
                slic1_flag=False
        
            if slic3_flag:
                if slic_pstart < idx:
                    # print(f'Append missing data btw idx slic3 {slic_pstart}:{idx} {word[slic_pstart:idx]}' )                                                    
                    tokens.append(word[slic_pstart:idx])
                tokens.append(slic3)                
                slic_pstart=idx+1 + len(slic3)-1
                # print(f'At index {idx} :Need to split3 at {slic3}' )
            else:
                if slic2_flag:
                    if slic_pstart < idx:
                        # print(f'Append missing data btw idx slic2 {slic_pstart}:{idx} {word[slic_pstart:idx]}' )                                    
                        tokens.append(word[slic_pstart:idx])            
                    # if slic_pstart <idx+1:
                    tokens.append(slic2)
                    slic_pstart=idx+len(slic2)       
                    # print(f'slic2 pstart:{slic_pstart}')
                    # print(f'At index {idx} :Need to split2 at {slic2} and set next start point: {idx+1+len(slic2)} and it value:{word[idx+len(slic2)]}' )                
                else:
                    if slic1_flag:
                        if slic_pstart < idx:
                            tokens.append(word[slic_pstart:idx])
                            # print(f'Append missing data btw idx slic1 {slic_pstart}:{idx} {word[slic_pstart:idx]}' )                                    
                        if slic_pstart<=idx:
                            tokens.append(slic1)
                            slic_pstart=idx+1 + len(slic1)-1
                            # print(f'At index {idx} :Need to split1 at {slic2}' )                                    
        return tokens

    def iast2tokens(word):
        if len(word) <=1:
            return word
    # def iast2tokens(vowel_plist,consonant_list,  word):        
        vowel_plist=IAST.vowel_plist
        consonant_list=IAST.consonant_list

        iast_tokens= []
        vowel_tokens = IAST.lex_iast(vowel_plist,word)
        # print(vowel_tokens)
        if word[-1*len(vowel_tokens[-1]):]==vowel_tokens[-1]:
            pass
            # print('Last word match with vowel no need to append')
        else:
            vowel_tokens.append(word.split(vowel_tokens[-1])[-1])
            # print('need to append')
            # print(vowel_tokens)
        for i in vowel_tokens:
            # print(i, lex_iast(consonant_list,i))
            if len(IAST.lex_iast(consonant_list,i)) <=1:
                iast_tokens.append(i)
            else:
                iast_tokens.extend(IAST.lex_iast(consonant_list,i))
        return iast_tokens


    def tokens2dict_tokenes(self,tokens,indic_lang):
        input_tokens=''
        output_string = []
        for token in tokens:
            # query_bara = f"""SELECT IAST,{indic_lang} FROM {self.barakhadi} WHERE IAST LIKE '%{token}'"""
            # query_alpha = f"""SELECT type, IAST,{indic_lang} FROM {self.alphabet} WHERE IAST LIKE '{token}%'"""
            query_bara = f"""SELECT IAST,{indic_lang} FROM {self.inv_barakhadi} WHERE IAST ='{token}'"""
            query_alpha = f"""SELECT type, IAST,{indic_lang} FROM {self.inv_alphabet} WHERE IAST='{token}'"""

            # print(query_bara)
            # print(query_alpha)
            data_alpha = self.get_query(query_alpha)
            data_bara = self.get_query(query_bara)
            # print(data_bara)
            input_tokens += token+ ' '
            # print(token,'Alphabets: ', data_alpha,' Barakadi',data_bara)
            temp_dic = dict()
            temp_dic['IAST']=token
            temp_dic['lang']=indic_lang
        # type, alph, bara are enter below 
            # temp_dic['type']=
            # temp_dic['alph']=
            # temp_dic['bara']= 
            if len(data_alpha):
                temp_dic['type']=data_alpha[0]['type']
                # temp_dic['alph']=data_alpha[0][indic_lang] # wrong method if token = n ,n̆ḍa, n̆ja then : 
                # we 1st search result is none which we need to filter
                for entry in data_alpha: 
                    if entry[indic_lang] is not None :                        
                        # print(entry[indic_lang],entry['IAST'],entry['type'])
                        temp_dic['alph']=entry[indic_lang]
                        temp_dic['type']=entry['type']
                        break  
                    else:
                        # print(f'In entry:{entry} indic_lang: {indic_lang} is None need to update dic')
                        temp_dic['alph']=entry[indic_lang]
                        temp_dic['type']=entry['type']
                        break
    
                # output_string +=' | '+ data_alpha[0][indic_lang]+' : '  +data_alpha[0]['type'] +' | '
            else:
                temp_dic['alph']=None
            if len(data_bara):
                # output_string +=' | '+ data_bara[0][indic_lang] +' | '
                temp_dic['type']='vowel'
                temp_dic['bara']=data_bara[0][indic_lang]
            else:
                temp_dic['bara']=None
            output_string.append(temp_dic)
        return output_string
        
    def get_indic_halant(self,indic_lang):
        query_alpha = f"""SELECT IAST,{indic_lang} FROM {self.barakhadi} WHERE IAST='ŭ'"""
        data_alpha = self.get_query(query_alpha)
        halant = self.get_query(query_alpha)[0][indic_lang]
        return halant

    
    def dict_tokens2indic(output_string,halant):
                            #'क'+  'ा'+'ः' #>>>  'काः'
                            #'क'+'्'   # >>> 'क्'
                            #'क्'+ 'ा' # >>> 'क्ा'
                            
        output=''
        for idx, item in enumerate(output_string):
            print_status = False    
            # print(idx, item)
            if idx ==0:
                prev_item=dict()
            else:
                prev_item=output_string[idx-1]
            if idx < len(output_string)-1:
                
                next_item = output_string[idx+1]
            elif idx ==len(output_string)-1:
                next_item = dict()
                
            if 'type' in item.keys() and item['type']=='consonants':
                if 'type' in next_item.keys() and next_item['type']=='vowel':
                    # print(item['alph'], end=" ")
                    if item['alph'] is not None :
                        output +=item['alph']
                        print_status =True
                elif 'type' in next_item.keys() and next_item['type']=='consonants':
                    # print(item['alph']+halant,end="")
                    if item['alph'] is not None :
                        output +=item['alph']+halant
                        print_status =True
                elif 'type' not in next_item: # word ending with consonant and halant
                    if item['alph'] is not None :
                        output +=item['alph']+halant
                        print_status =True
                    
                    
            if 'type' in item.keys() and item['type']=='vowel':
                # print('ITEM: ',item)
                # print('PREV ITEM: ',prev_item)
                if 'type' in prev_item.keys() and prev_item['type']=='consonants':
                    # print(item['bara'], end=' ')
                    if item['IAST']=='a':
                        print_status =True                            
                        pass
                    else:        
                        if item['bara'] is not None :                                            
                            output +=item['bara']
                            print_status =True            
                    # print(item)

                if 'type' in prev_item.keys() and prev_item['type']=='vowel':
                    if item['bara'] is not None :                    
                        output +=item['bara']            
                        # print(item)
                        print_status =True
                # pass
                if 'type' not in prev_item : # starting of word or starting of line
                    if item['alph'] is not None :
                        output +=item['alph']                            
                        print_status =True                
        
            
            if not print_status:
                output +=item['IAST']
            # print(output)
        return output
    
    # def iast2indic(self,vowel_plist,consonant_list,word,indic_lang):    
    def iast2indic(self,word,indic_lang):
        vowel_plist=IAST.vowel_plist
        consonant_list=IAST.consonant_list
        if len(word)==0:
            return word
        tokens= IAST.iast2tokens(word)
        # tokens= IAST.iast2tokens(vowel_plist,consonant_list,  word)
        # print(tokens)
        dict_tokene_list = self.tokens2dict_tokenes(tokens,indic_lang)
        # print(output_string)
        # halant=self.get_indic_halant(indic_lang)
        query_alpha = f"""SELECT IAST,{indic_lang} FROM {self.inv_barakhadi} WHERE IAST='ŭ';"""
        data_alpha = self.get_query(query_alpha)
        halant = self.get_query(query_alpha)[0][indic_lang]
        # print(halant)
        output=IAST.dict_tokens2indic(dict_tokene_list,halant)
        return output
