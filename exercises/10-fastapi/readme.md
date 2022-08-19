# FastAPI Exercises

Let's put the pieces together in this FastAPI section. Recall that FastAPI is built from:

* Python typing
* Pydantic
* async/await
* Likely need for *some* database (we used Beanie)

We have already covered these and aquired decent expeirence with all of them. FastAPI is just a clever way of putting these to work together.

## The world needs to calculate

To start small, let's create a calculator API. Using a url pattern like:

```
http://localhost:8000/api/calculator/add/7/11
```

To add `7 + 11-> 18` is probably the simpliest. But you could go adventurous and accept a JSON object as a POST to `http://localhost:8000/api/calculator`:

```json
{
  "x": 7,
  "y": 11
}
```

 Take your pick. But start from an empty Python file and new virtual environment. Remember to get started you'll need `pip install fastapi uvicorn` as the base libraries.

Create a app and run it with uvicorn. Add a single endpoint (either GET or POST as discussed above), then test it out. 

## Validating data

Let's assume you go the GET route and use the URL pattern:

```
http://localhost:8000/api/calculator/add/X/Y
```

What happens if `X = "7"` is submitted? How about `X = "seven"`. If the "response" is 500 server error, that's bad. If it's `404 NOT FOUND`, that's less bad. But wouldn't it be better to tell the caller the data they gave was bad? That's probably either status code 422 or another 400 code (see [httpstatuses.io](https://httpstatuses.io) and make the call).

Update your add API endpoint to return a meaningful error to bad data like this. Hint: FastAPI *may* handle this for you automatically if you define the API endpoint correctly.

## The world also needs auditing

In addition to just processing the results in memory and returning the sum, we want to save our requests to the database with an ID (who knows, maybe we need to come back to them).

Bring over all the `Beanie` and `mongo_setup.py` code we've used (not the models, just the setup / connection code). Create a `beanie.Document` class. It should save `x`, `y`, and `created` for each add request and the API should return the DB `id` as a string so the caller knows about which record is there. 

Rather than returning `18`, how about something like:

```json
{
  "request_id": "62fef09ba6209c01fd636e42",
  "created": "2022-08-18",
  "x": 7,
  "y": 11,
  "action": "add",
  "result": 18
}
```

Remember, you'll need to use `async` methods and `await` the beanie calls. And, hint, a pydantic model matching the above would be helpful.

## The world also needs documentation

Finally, set the `response_model` property in the `@app.get()` or `@app.post()` call to document the schema you come up with above. Check `http://localhost:8000/docs` to see the doc page.

## Solutions

For *a* solution, look in the `./solution` folder next to this file.

