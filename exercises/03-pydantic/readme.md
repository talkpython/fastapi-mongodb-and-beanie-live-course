# Pydantic Exercises

In this exercise, you will define some pydantic models and parse and validate JSON data.

## Steps

* Open the folder `pydantic_exercise` and open `parser.py`. 
* Create a virtual environment, activate it, then install `pydantic`.
* Use the following code to load the `pydantic.json` file into memory as a dictionary.

```python
file = Path(__file__).parent / 'pydantic.json'
with open(file, 'r', encoding='utf-8') as fin:
    data = json.load(fin)
```

* Next, study the `pydantic.json` file. You will need to create pydantic models to load it.
* Create your model class(es). Recall those are of the format:

```python
class Package(pydantic.BaseModel):
  name: str
  summary: str
  release_count: Optional[int]
  # ...
```

* Do a little by hand, but then consider something like **[jsontopydantic.com](https://jsontopydantic.com)** to speed you along.
* Load the model from the dictionary by "exploding" the dictionary: `package = PackageModel(**data)`
* Use the `package` object to print some info about the package.

## Solutions

The solution (*a solution*) is in the `./solution` folder.

