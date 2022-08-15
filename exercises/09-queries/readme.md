# Working with data in Beanie Exercises

Now it's time to insert the starter data, run some queries, then even insert new data.

## Loading PyPI Data into MongoDB

I've downloaded a ton of data from PyPI and organized it into JSON documents. These are the top 5,000 most popular packages at the time of downloading. Get this collection of data as a zip file:

[https://talk-python-course-videos.nyc3.digitaloceanspaces.com/resources/pypi-top-5k.zip](https://talk-python-course-videos.nyc3.digitaloceanspaces.com/resources/pypi-top-5k.zip)

Once you download it, unzip it to a location where you can temporarily leave it while importing data. It won't be needed after that.

To import the data, just run the file `load_data.py` in the code folder: `code/09-beanie-querying/bin`. Be sure to do this using the `code/09-beanie-querying` folder as the working directory or if you have it open in PyCharm, mark that folder as the **sources root**.

In order for this to work, you'll need to have the MongoDB server running. Recall from the discussion today, it may or may not auto start, depending on the platform, how in installed it, and what you've done since then. So to run MongoDB the server:

* macOS (via Homebrew): `brew services start mongodb-community` 
* Linux (via apt, etc): `sudo systemctl start mongod`
* Windows: Open `services` command panel, find MongoDB, press the start button if it's not running

Run the program as described above. Then open your management tool of choice (e.g. Robomongo) and verify there is data in the server.

## Querying the database

For our demos today, we started with an empty structure of a program that asked questions about our data (like number of packages and users, etc). For your homework, you'll start with that empty project again and create it from scratch.

Feel free to use the final code I checked in today as well as the slides from today to figure out what code you need.

Look in the folder:

`exercises/09-queries/query_starter` 

There's the file `beanie_querying_app.py`. Start there and implement the functions needed in the two `services` files. Again, that top-level folder (`query_starter`) will need to be the sources root.



## Solutions

For solutions, look at the final code at `code/09-beanie-querying/beanie_querying_app.py` and files in the folders there.

