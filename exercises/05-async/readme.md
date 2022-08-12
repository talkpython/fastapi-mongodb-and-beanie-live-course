# Async Exercises

In this exercise, you will use async/await to work with external APIs in-bulk.

We will use the [Talk Python weather API](https://weather.talkpython.fm) to access the weather for multiple locations. Doing this in serial (synchronous code) can be somewhat slow. Using async will allow us to get results for all locations at once.

## Steps

* Create a new folder/project where you can write some code.
* Create a `main.py` file to write your code in.
* Create a virtual environment, activate it, then install `httpx` (needed for async web calls).
* We want the weather for the following locations:
  * Portland, OR
  * Seattle, WA
  * La Jolla, CA
  * Phoenix, AZ
  * New York, NY
  * Boston, MA

* To access the weather for any location, we'll use the URL:

```python
https://weather.talkpython.fm/api/weather?city=CITY&state=STATE_ABBREVIATION&country=US&units=imperial
# Units imperial or metric
```

* Write a function that takes the city and state to get the weather. This should be an ***async*** method.  You will also need to pull the relevant information out of the dictionary you receive from the API.  Recall that async methods look like:

```python
async def some_function(arg1, arg2):
    sync_code()
    await async_code()
    
    return value
```

* To implement this code, you'll need to use **[httpx](https://github.com/encode/httpx)**. The code should be quite similar to what we did accessing the titles of Talk Python episodes. So feel free to leverage the structure and examples from our **[live code here](https://github.com/talkpython/fastapi-mongodb-and-beanie-live-course/blob/2022-08/code/05-async/web-scraper/async_scrape/program.py)**.

## Solutions

The solution (*a solution*) is in the `./solution` folder.

