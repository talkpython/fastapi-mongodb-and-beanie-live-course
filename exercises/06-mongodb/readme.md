# MongoDB Exercises

Now it's time to install and connect to MongoDB.

## Installing MongoDB

The steps to install MongoDB differs a lot across OSes. Just visit the [**MongoDB Installation Tutorials**](https://www.mongodb.com/docs/manual/installation/) page, find your OS, and follow along. Of course, you're welcome to use an alternative method if you have experience or want to experiment.

Personally, my best experience has been with:

* macOS -> via homebrew (described in the page above)
* Windows -> via the MSI installer on [this page](https://www.mongodb.com/try/download/community)
* Linux -> via the os package manager

## Installing management tools

While we will primarily be using Python + Beanie to talk with Mongo, you'll need to check in on it using some more general tools from time to time. That's where the management tools come in. 

If you'd like to have access to the management tools (recommended), then [install them as described here](https://www.mongodb.com/docs/mongodb-shell/install/#std-label-mdb-shell-install). This is where you get `mongosh` that you saw me use but also utilities for backing up and restoring Mongo.

You'll also want a better UI-oriented tool for day to day work with the database. Options include:

* **Robomongo** (free, open source): Download the latest release from [their github page](https://github.com/Studio3T/robomongo/releases).
* **PyCharm Pro** / **DataGrip** (paid): If you have PyCharm pro, they have MongoDB support built it. They have [a great write up about it](https://blog.jetbrains.com/datagrip/2020/06/16/introducing-mongodb-shell-in-datagrip/).
* **[MongoDB's own Compass](https://www.mongodb.com/products/compass)**: Nice, but less "shell/CLI-oriented" (for example, [see this screen shot](https://www.mongodb.com/docs/compass/current/query/skip/) for the query builder). It may work well for you, but I recommend the tools above.

## Connections

Once you get Mongo setup and running (on macOS and Linux you have to start the server afterwards), you should be able to connect to it. In RoboMongo, just use these settings:

* Type: direct
* Name: local
* Address: localhost
* Port: 27017

Defaults on everything else. You can adapt these to the other tools if you chose something else.

Make sure you can connect and get to the server.

