# Load Testing Exercises

Building a functional API or web app is easy enough in FastAPI. But will it work for your situation? How many users can it handle? Do you need to spend for higher-end hardward? Is it fast enough to avoid adding [caching layers](https://betterprogramming.pub/how-to-use-redis-for-caching-and-pub-sub-in-python-3851174f9fb0) - your app will be much simpler if you can.

We'll answer that quesiton in this chapter. We chose [locust.io](https://locust.io) as our load testing framework. It has a great runner, it can scale large enough across machines to generate massive load if needed, and it's programmed with Python.

## Defining your test mix

To create a set of tests in Locust, just create a Python class. It's easiest if this is in a file called `locustfile.py`. It doesn't matter where this is located but you should run it with locust installed in that version of Python.

```python
import locust

class ApiTesterMix(locust.FastHttpUser):
  host = 'http://localhost:8000'
  
  # ...
```

Then for each scenario you want to test, add a decorated method to the class:

```python
@locust.task()
def some_scenario():
    client.get(url1)
    client.get(url2)
    client.get(url3)
```

## Testing your API

Think of the different ways people could use the API we created in the class. Separately start that PyPI API running, then add the test mix to a locust class. Remember you can pass `weight=N` to the task decorator to adjust the frequency of each method.

Once you have few scenarios added, run the test by simply typing `locust` with the venv active in the same directory as the `locustfile.py`. Then use the interactive web app to run your tests.

## Improving performance

We saw that some methods are faster and others slower. Can you tweak the API code to make it faster and prove it with locust? Ideas include:

* Adding new indexes
* Using projections to limit the data returned
* Adding a full-text search for the search command
  * See Beanie's `Text` criteria: https://roman-right.github.io/beanie/api-documentation/operators/find/#text
  * Along with the index type `pymongo.TEXT`

Example for full text search from Beanie:

```python
class Sample(beanie.Document):
    description: beanie.Indexed(str, pymongo.TEXT)

async def coffees():
	return await Sample.find(beanie.Text("coffee")).to_list()
```

Make some changes to the code and see if you get better performance. Remember to just change one thing at a time and perhaps focus on one mix in locust at a time too. How much better can you make our app perform?

## More like production

Running in our dev server isn't how we'd run in production (although uvicorn is pretty good). Run a more scaled out, threaded version to test next. Close your running API. Then `pip install gunicorn` and run the command:

```
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
```

In the folder containing main.py for your API with the venv active.

Try testing again to see if you get better perf. Can you tweak the number of works (4 above) to find the optimal mix?

## Solution

For a solution, just look at our finished code: `code/12-load-testing/locustfile.py` from this repo.
