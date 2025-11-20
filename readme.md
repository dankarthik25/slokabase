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

# sudo cp slokabase_linux_app /usr/local/bin/slokabase      # : move file to local/bin/ and change file name
# OR: use  user space (~/.local/bin)   #Generally: user space is prefered
sudo cp slokabase_linux_app ~/.local/bin/slokabase        # : move file to home local bin and change file
cd ~/.local/bin/slokabase
chmod +x slokabase_linux_app                              # : make this file executable 

# Now you can run app from anywhere in cli 
slokabase # run in terminal
```
# Project Progress
