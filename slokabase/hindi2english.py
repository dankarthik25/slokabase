def hindi2iast(text):
    index_dic ={'अ': 'a', 'आ': 'ā', 'ॲ': 'ê', 'ऑ': 'ô', 'इ': 'i', 'ई': 'ī', 'उ': 'u', 'ऊ': 'ū', 'ऋ': 'ṛ', 'ॠ': 'ṝ', 'ऌ': 'ḷ', 'ॡ': 'ḹ', 'ए': 'e', 'ऎ': 'ē', 'ऐ': 'ai', 'ओ': 'o', 'ऒ': 'ō', 'औ': 'au', 'अं': 'aṁ', 'अः': 'aḥ', 'ॐ': 'oṁ', 'क': 'ka', 'ख': 'kha', 'ग': 'ga', 'घ': 'gha', 'ङ': 'ṅa', 'च': 'ca', 'छ': 'cha', 'ज': 'ja', 'झ': 'jha', 'ञ': 'ña', 'ट': 'ṭa', 'ठ': 'ṭha', 'ड': 'ḍa', 'ढ': 'ḍha', 'ण': 'ṇa', 'त': 'ta', 'थ': 'tha', 'द': 'da', 'ध': 'dha', 'न': 'na', 'प': 'pa', 'फ': 'pha', 'ब': 'ba', 'भ': 'bha', 'म': 'ma', 'य': 'ya', 'र': 'ra', 'ल': 'la', 'व': 'va', 'श': 'śa', 'ष': 'ṣa', 'स': 'sa', 'ह': 'ha', 'क्ष': 'kṣa', 'ज्ञ': 'jña', 'ऽ': '’', '०': '0', '१': '1', '२': '2', '३': '3', '४': '4', '५': '5', '६': '6', '७': '7', '८': '8', '९': '9', '।' :'|', '॥':'||'}
    barakhadi = {'ा': 'ā', 'ॅ': 'ê', 'ॉ': 'ô', 'ि': 'i', 'ी': 'ī', 'ु': 'u', 'ू': 'ū', 'ृ': 'r̥', 'ॄ': 'r̥̄', 'ॢ': 'l̥', 'ॣ': 'l̥̄', 'ॆ': 'e', 'े': 'ē', 'ै': 'ai', 'ो': 'o', 'ौ': 'au', 'ं': 'aṁ', 'ः': 'aḥ', ':': 'ḥ'}
    output_text = ''
    for line in text.split('\n'): 
        for i in line:
            # print(ord(i), i)
            if i in index_dic.keys():
                output_text += index_dic[i]
                # print(index_dic[i], end='')
            elif i == '्' and output_text[-1] == 'a':
                output_text = output_text[:-1]
                # print('error')
            elif i in set(barakhadi.keys()) and output_text[-1] == 'a':
                # print(i)
                output_text = output_text[:-1] + barakhadi[i]
            elif i ==':' or ord(i) == 2307: # 2307 ः
                output_text += 'ḥ' 
            elif ord(i) == 2306 : # i == ं  or  ं, aṁ
                output_text += 'ṁ'
            elif ord(i) == 8205 :# and outpu2307 ःt_text[-1] == 'a':# i == ं ू , ū
                # https://en.wikipedia.org/wiki/Zero-width_joiner
                pass
            else :
                # print('else ',i, ord(i))
                output_text += i
                # print(i,end='')
        output_text+= '\n'    
    return output_text
