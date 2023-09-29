
# Steps during creation of project  
```sh

# 1st step to create env if not exist and install package
#  conda create --name vedabase  

# Open the env and install package and save env-file

conda env create -f environment.yml  # create env with existing env file
conda activate vedabase

# conda env export --no-builds > environment.yml # to export env 

# Run flask 


conda activate vedabase
# method 1

flask run

# method 2
python main.py
python run.py # To run the code       : To view existing songs but not for adding new songs


```
# Project Progress
## `DONE` Add new songs to Flask App

1. `DONE` Get website containting all the song and Translation :  
eg : http://kksongs.org/songs/p/pralayapayodhijale.html 
2. `DONE` Automate web scrapping  for getting the song and Translation to loading in **Database**

## `TODO` Convert deva-nagri language to iskcon-font type:
there are may non iskcon song which don't follow them so we need to covert them to hin-glish (iskcon-font)
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




