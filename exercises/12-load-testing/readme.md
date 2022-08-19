# Load Testing Exercises





Notes for full text search:



```python
class Sample(Document):
    description: Indexed(str, pymongo.TEXT)

await Sample.find(Text("coffee")).to_list()
```

