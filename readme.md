
# Steps during creation of project  
```sh

# 1st step to create env if not exist and install package
#  conda create --name vedabase  

# Open the env and install package and save env-file

conda env create -f environment.yml  # create env with existing env file
conda activate vedabase


# method 2
python run.py # To run the code       : To view existing songs but not for adding new songs

# conda env export --no-builds > environment.yml # to export env 

# Run flask 


conda activate vedabase
# method 1

flask run


```
# Project Progress
## `DONE` Add new songs to Flask App

1. `DONE` Get website containting all the song and Translation :  
eg : http://kksongs.org/songs/p/pralayapayodhijale.html 
2. `DONE` Automate web scrapping  for getting the song and Translation to loading in **Database**

## `TODO` Convert deva-nagri language to iast-font type:
there are may non iskcon song which don't follow them so we need to covert them to hin-glish (iast-font)
 we can get directly from vedabase with hindi and hin-glish.

## `TODO` For newly added songs we need to automate word-to-word meaning
split the verse into word and search each word in dictionary. For that we need dictionary


## `TODO` Create a dictionary simillar to vedabase
Need to web scrape vedabase for bg,cc, sb....etc to get the word to word meaning 

Create a Dictionary 




# Create db using sql alchemy and flask 

https://stackoverflow.com/questions/34122949/working-outside-of-application-context-flask


# Flask Example in github
https://github.com/MyAwesomeNote/flask-app/blob/master/apps/crud/views.py




# Add songs to your database 
http://kksongs.org/synonym/


All songs with synonym

["adharammadhuram.html", "akrodhaparamananda.html", "amarjivan.html", "amijamunapuline.html", "antaramandire.html", "arkotokal.html", "bhajabhakatavatsala.html", 
"bhajahuremana.html", "borosukherkhaborgai.html",
"cetodarpana.html", 
"eibarokarunakoro.html", "emonadurmati.html", 
"gaurangabolitehabe.html", "gaurangakorunakoro.html", "gaurangerdutipada.html", "gaygoramadhursware.html", "gopinath1.html", "gopinath2.html", "gopinath3.html", "gurudeva4.html",
"hariharayenamah.html", "harihari04a.html", "harihedoyalmora.html", "haritumharo.html", "hegovindahegopal1.html", "hegovindahegopala3.html", "jayagovindajayagopala.html", "jayajayagoracander.html", "jayamadhavamadana.html", "jayaradhagirivara.html", "jayaradhamadhava.html", "jayaradhejayakrsna1.html", "jayaradhejayakrsnajayavrndavana3.html", "jeanilopremadhana.html", "jivjago.html", 

"maineratanalagai.html", "mamamanamandire.html", "manasadehogeho.html", "muralimanoharagopala.html", 
"namamisvaram.html", "namastenarasimhaya.html","nitaipadakamala.html", "naradamuni.html", 
"ohevaisnava.html", 
"paramakaruna.html", "pralayapayodhijale.html", 
"radhakrsnabol.html", "radhakrsnapranamora.html", "radhejayajayamadhava.html", 
"sabseoonchi.html", "samsaradavanala.html", "srigurucaranapadmakevala.html", "srikrsnacaitanyaprabhudoya.html", "srirupamanjaripada.html", "sritakamala.html", "suddhabhakata.html", "sujanarvudaradhitapada.html", "sulabhobhaktiyuktanam.html", "sundaramor.html", "tummerirakholajahari.html",
"udiloaruna.html", 
"vamsidharikrsna.html", "vibhavarisesa.html", "vidyaravilase.html", "vrndavanaramyasthana.html", 
"yasomatinandana.html"] 

song_list:  ['/synonym/hegovindahegopala3.html', '/synonym/kabegauravane.html', '/synonym/kabehabebolo.html', '/synonym/krsnahoitecaturmukha.html', '/synonym/krsnotkirtanagananartana.html', '/synonym/namonamahtulasikrsna1.html', '/synonym/namonamahtulasimaharani.html', '/synonym/nitaipadakamala.html']

"hegovindahegopala3.html",
"kabegauravane.html","kabehabebolo.html","krsnahoitecaturmukha.html","krsnotkirtanagananartana.html",
"namonamahtulasikrsna1.html","namonamahtulasimaharani.html","nitaipadakamala.html"



"adharammadhuram-synonym.txt",
"akrodhaparamananda-synonym.txt",
"amarjivan-synonym.txt",
"amijamunapuline-synonym.txt",
"antaramandire-synonym.txt",
"arkotokal-synonym.txt",
"bhajabhakatavatsala-synonym.txt",
"bhajahuremana-synonym.txt",
"borosukherkhaborgai-synonym.txt",
"cetodarpana-synonym.txt",
"eibarokarunakoro-synonym.txt",
"emonadurmati-synonym.txt",
"gaurangabolitehabe-synonym.txt",
"gaurangakorunakoro-synonym.txt",
"gaurangerdutipada-synonym.txt",
"gaygoramadhursware-synonym.txt",
"gopinath1-synonym.txt",
"gopinath2-synonym.txt",
"gopinath3-synonym.txt",
"gurudeva4-synonym.txt",
"hariharayenamah-synonym.txt",
"harihari04a-synonym.txt",
"harihedoyalmora-synonym.txt",
"haritumharo-synonym.txt",
"hegovindahegopal1-synonym.txt",
"hegovindahegopala3-synonym.txt",
"jayajayagoracander-synonym.txt",
"jayamadhavamadana-synonym.txt",
"jayaradhagirivara-synonym.txt",
"jayaradhamadhava-synonym.txt",
"jayaradhejayakrsna1-synonym.txt",
"jayaradhejayakrsnajayavrndavana3-synonym.txt",
"jeanilopremadhana-synonym.txt",
"jivjago-synonym.txt",
"kabegauravane-synonym.txt",'
"kabehabebolo-synonym.txt",
"krsnahoitecaturmukha-synonym.txt",
"krsnotkirtanagananartana-synonym.txt",
"maineratanalagai-synonym.txt",
"mamamanamandire-synonym.txt",
"manasadehogeho-synonym.txt",
"muralimanoharagopala-synonym.txt",
"namamisvaram-synonym.txt",
"namastenarasimhaya-synonym.txt",
"namonamahtulasikrsna1-synonym.txt",
"namonamahtulasimaharani-synonym.txt",
"naradamuni-synonym.txt",
"nitaipadakamala-synonym.txt",
"ohevaisnava-synonym.txt",
"sabseoonchi-synonym.txt",
"samsaradavanala-synonym.txt",
"srigurucaranapadmakevala-synonym.txt",
"srikrsnacaitanyaprabhudoya-synonym.txt",
"srirupamanjaripada-synonym.txt",
"sritakamala-synonym.txt",
"suddhabhakata-synonym.txt",
"sujanarvudaradhitapada-synonym.txt",
"sulabhobhaktiyuktanam-synonym.txt",
"sundaramor-synonym.txt",
"tummerirakholajahari-synonym.txt",
"udiloaruna-synonym.txt",
"vamsidharikrsna-synonym.txt",
"vibhavarisesa-synonym.txt",
"vidyaravilase-synonym.txt",
"vrndavanaramyasthana-synonym.txt"
"yasomatinandana-synonym.txt"