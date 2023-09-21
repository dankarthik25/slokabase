```
 conda create --name vedabase  
 conda env export --no-builds > environment.yml
```

# To recreate the same env
```conda env create -f environment.yml
```

# Run flask 
```
conda activate vedabase
# method 1
flask run

# method 2
python main.py

```



# Create db using sql alchemy and flask 

https://stackoverflow.com/questions/34122949/working-outside-of-application-context-flask


# Flask Example in github
https://github.com/MyAwesomeNote/flask-app/blob/master/apps/crud/views.py




CREATE TABLE song_idx (
	song_idx INTEGER PRIMARY KEY, 
	song_name VARCHAR(100) NOT NULL UNIQUE, 
	song_short_name VARCHAR(100) NOT NULL UNIQUE, 
	division VARCHAR(100), 
	division_no VARCHAR(100), 
	sloka_statues BOOLEAN NOT NULL CHECK (sloka_statues IN (0, 1)) ,
	total_slokas INTEGER, 
    groups VARCHAR(100), 
	devotion_god VARCHAR(100), 
	author VARCHAR(100), 
	describtion TEXT, 
	other_links TEXT
);


CREATE TABLE [IF NOT EXISTS] [schema_name].table_name (
	column_1 data_type PRIMARY KEY,
   	column_2 data_type NOT NULL,
	column_3 data_type DEFAULT 0,
	table_constraints
) [WITHOUT ROWID];

CREATE TABLE contacts (
	contact_id INTEGER PRIMARY KEY,
	first_name TEXT NOT NULL,
	last_name TEXT NOT NULL,
	email TEXT NOT NULL UNIQUE,
	phone TEXT NOT NULL UNIQUE
);