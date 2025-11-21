
# <span style='font-family: "Devonshire", cursive;   font-weight: 400; font-style: normal; font-size: 45px; color: #94492c;'>Śloka Space</span>
For Static Web Pages Visit : https://dankarthik25.github.io/SlokaSpace/index.html <br>
Sloka Space is a digital platform for organizing, studying, and preserving *slokas*, chants, and verses from Vedic and spiritual traditions.  
It provides a structured way to store scriptures, translations, and metadata with a fast, secure local database.

Sloka Space is built for **learners**, **teachers**, and **practitioners** who want a clean, modern interface for accessing traditional knowledge.
<img src="images/SlokaSpace.gif" style="width:683px;height:384px; display: block;margin-left: auto; margin-right: auto;" alt="alt text" title="Caption">




## ✨ Features

### 📚 Sloka Library
- Store slokas from scriptures such as the Bhagavad Gita, Upanishads, Stotras, Bhajans, and more  
- Structured format: *Scripture → Chapter → Sloka*  
- Multi-language support: Sanskrit, Hindi, English  
- Transliteration and word-by-word meanings  
- Synonyms and commentary support

### 🔍 Search & Filter
- Fast full-text search  
- Filter by scripture, chapter, deity, category, or metadata  
- Optimized lookup using SQLite indexes



### 💾 Offline Storage
- Fully offline-capable  
- SQLite backend  

### TODO: 🎧 Audio Support
- Attach audio recitations  
- Practice mode (looping, repeat counts)  
- Adjustable playback speed

### TODO: 📝 Study Tools
- Add personal notes  
- Highlight slokas  
- Save favorites  
- Collections/playlists for chanting  
- Track learning progress




# User Installation 
##  using python
```sh
# 1st step to create env if not exist and install package
# git clone 
cd slokabase
conda env create -f environment.yml  # create env with existing env file
conda activate vedabase


# method 2
flask run  # or RUN BELOW CMD 
python app.py # To run the code       : To view existing songs but not for adding new songs
```

## Using Docker 
```sh
# git clone 
cd slokabase
# docker image build (Note: DOCKERFILE file should exist in current folder)
docker build --tag slokabase_img .
docker run -itd --name sloka_con -p 5000:5000 slokabase_img  # For read only 
# open localhost:5000

# For Persistane Storage 
docker run -it --name sloka_con -v ./database:/app/database -p 5000:5000 slokabase_img 
# OR 
docker run -it --name sloka_con -v database_path:/app/database -p 5000:5000 slokabase_img 
```

## Using Linux CLI
```sh
#>>> head -n12 slokabase_linux_app 
  
# bash Script Info:  It is  Dockerized CLI wrapper with cleanup for Slokabase

# sudo cp slokabase_linux_app /usr/local/bin/slokabase      
        # : move file to local/bin/ and change file name
# OR: use  user space (~/.local/bin)   
        #Generally: user space is prefered
sudo cp slokabase_linux_app ~/.local/bin/slokabase        
        # : move and rename file to home > .local > bin > (slokabase) 
cd ~/.local/bin
chmod +x slokabase                              
        # : make this file executable 

# Now you can run app from anywhere in cli 
slokabase # run in terminal
```